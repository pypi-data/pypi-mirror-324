import express from "express";
import { readFileSync } from "fs";
import { randomUUID } from "node:crypto";
import { fetch } from "http-signed-fetch";
import bodyParser from "body-parser";
import { createHash } from "crypto";

const publicKey = readFileSync("public_key.pem", "ascii");
const privateKey = readFileSync("private_key.pem", "ascii");

const keypair = { privateKeyPem: privateKey };

const app = express();

const port = 80;
const host = "cattle_grid_demo";
const username = "jskitten";
const publicKeyId = `http://${host}/actor#main-key`;
const jskitten = `http://${host}/actor`;

const makeId = () => {
  return `http://${host}/` + randomUUID();
};

const computeSha256Digest = (body) => {
  const sha256 = createHash("sha256");
  sha256.update(body);
  return sha256.digest("base64").toString();
};

const getInbox = async (actor) => {
  const response = await fetch(actor, {
    headers: {
      accept: "application/activity+json",
    },
    method: "get",
    publicKeyId,
    keypair,
  });
  console.log(response);
  const parsed = await response.json();
  return parsed.inbox;
};

const postInbox = async (inbox, data) => {
  const response = await fetch(inbox, {
    headers: {
      "Content-Type": "application/activity+json",
    },
    method: "post",
    body: JSON.stringify(data),
    publicKeyId,
    keypair,
  });
  console.log(response);
};

app.get("/.well-known/webfinger", (req, res) => {
  res.send({
    links: [
      {
        href: `http://${host}/actor`,
        rel: "self",
        type: "application/activity+json",
      },
    ],
    subject: `acct:${username}@${host}`,
  });
});

app.get("/actor", (req, res) => {
  console.log("Get actor");
  console.log(req.headers);
  res.send({
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://w3id.org/security/v1",
    ],
    id: `http://${host}/actor`,
    type: "Service",
    inbox: `http://${host}/inbox`,
    outbox: `http://${host}`,
    preferredUsername: username,
    name: "Javascript Kitten",
    summary:
      "<p>I'm just a cute kitten meowing whenever, I get a message.</p><p>Please help me cross the <a href='https://codeberg.org/bovine/cattle_grid/'>cattle grid</a>. I also like cow milk.</p>",
    publicKey: {
      id: `http://${host}/actor#main-key`,
      owner: `http://${host}/actor`,
      publicKeyPem: publicKey,
    },
  });
});

const rawParser = bodyParser.raw({ type: "*/*" });
app.post("/inbox", rawParser, (req, res) => {
  console.log("post");
  console.log(req.headers);
  var requester = req.header("x-cattle-grid-requester");
  if (!requester) {
    res.status(401).send();
    return;
  }
  const digest = req.header("Digest");
  const computedDigest = computeSha256Digest(req.body);
  console.log("Got Digest " + digest + " computed " + computedDigest);
  const [algorithm] = digest.split("=", 1);
  const digestValue = digest.slice(8);
  if (algorithm.toLowerCase() !== "sha-256") {
    console.error("Wrong algorithm " + algorithm);
    res.status(401).send();
    return;
  }
  if (digestValue !== computedDigest) {
    console.error("Digest mismatch " + digestValue);
    res.status(401).send();
    return;
  }
  res.status(202).send("processing");

  (async () => {
    const body = req.body.toString();
    console.log(body);

    const parsed = JSON.parse(body);

    if (parsed.actor !== requester) {
      console.error("Wrong requester");
      return;
    }

    const inbox = await getInbox(parsed.actor);

    if (parsed.type === "Create") {
      const obj = parsed.object;
      if (obj.type === "Note") {
        const reply = {
          "@context": "https://www.w3.org/ns/activitystreams",
          id: makeId(),
          actor: jskitten,
          type: "Create",
          object: {
            id: makeId(),
            type: "Note",
            content: "meow",
            to: [parsed.actor, "as:Public"],
            tag: {
              type: "Mention",
              href: parsed.actor,
            },
            inReplyTo: obj.id,
          },
        };
        await postInbox(inbox, reply);
      }
    }
  })();
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
