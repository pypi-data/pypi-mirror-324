from cattle_grid.model.extension import MethodInformation

exchange_method_information = [
    MethodInformation(
        module="cattle_grid.exchange",
        routing_key="send_message",
        description="Takes an activity and sends it to its recipients",
    ),
    MethodInformation(
        module="cattle_grid.exchange",
        routing_key="update_actor",
        description="Updates an actor",
    ),
    MethodInformation(
        module="cattle_grid.exchange",
        routing_key="delete_actor",
        description="Deletes an actor",
    ),
]
