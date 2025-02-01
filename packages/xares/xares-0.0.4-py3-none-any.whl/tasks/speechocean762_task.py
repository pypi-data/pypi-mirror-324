from xares.task import TaskConfig


def speechocean762_config(encoder) -> TaskConfig:
    data_key = "accuracy"
    return TaskConfig(
        name="speechocean762",
        encoder=encoder,
        train_split="speechocean762_train",
        valid_split="speechocean762_test",
        test_split="speechocean762_test",
        zenodo_id="14725291",
        output_dim=1,
        metric="MSE",
        criterion="MSELoss",
        batch_size_encode=1,  # Just avoid padding for this task
        label_processor=lambda x: float(x[data_key]),
        do_knn=False,
        epochs=25,
    )
