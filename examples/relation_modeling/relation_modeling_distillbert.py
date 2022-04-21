import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset
from torch.optim import Adam
from torch import nn
import pytorch_lightning as pl
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertModel
from relation_modeling_utils import get_timestamp, load_fdata, load_data, Evaluator
from pytorch_lightning.loggers import WandbLogger
import wandb

MODEL_TYPE = "uncased"
NUM_EPOCHS = 3
BATCH_SIZE = 64
DATASET_TYPE = "n1"
FREEZE_EMB = False
LR_RATE = 1e-4

class DistilBERTHeadDataset(Dataset):
    def __init__(self, df, tokenizer_type="uncased"):
        self.tokenizer = DistilBertTokenizer.from_pretrained(f'distilbert-base-{tokenizer_type}')
        self.labels = np.asarray(df['label'].to_list())
        self.texts = [self.tokenizer(text, padding='max_length', max_length=32, truncation=True,
                                     return_tensors="pt") for text in df['text']]

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]


class DistilBERTClassifier(pl.LightningModule):
    def __init__(self, num_classes=3, dropout=0.5, learning_rate=1e-4, freeze_emb=False, model_type="uncased"):
        super().__init__()
        self.distilbert = DistilBertModel.from_pretrained(f'distilbert-base-{model_type}')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, num_classes)

        if freeze_emb:
            for parameter in self.distilbert.parameters():
                parameter.requires_grad = False
            self.classifier = nn.Sequential(self.linear)
        else:
            self.classifier = nn.Sequential(self.dropout, self.linear)

        self.criterion = nn.BCEWithLogitsLoss()
        self.learning_rate = learning_rate

        self.save_hyperparameters()
    
    def forward(self, input_ids, mask):
        outputs = self.distilbert(input_ids=input_ids, attention_mask=mask, return_dict=False)
        outputs = self.classifier(outputs[0][:, 0, :])
        return outputs

    def predict(self, input_ids, mask):
        return F.sigmoid(self.forward(input_ids, mask))
    
    def training_step(self, batch, batch_idx):
        X, y = batch
        mask = X['attention_mask']
        input_ids = X['input_ids'].squeeze(1)
        outputs = self.forward(input_ids, mask)
        train_loss = self.criterion(outputs, y.float())
        preds = F.sigmoid(outputs)
        self.log("train_loss", train_loss, on_epoch=True)
        self.log_metrics(preds, y, type="train")
        return train_loss
    
    def validation_step(self, batch, batch_idx):
        X, y = batch
        mask = X['attention_mask']
        input_ids = X['input_ids'].squeeze(1)
        outputs = self.forward(input_ids, mask)
        val_loss = self.criterion(outputs, y.float())
        preds = F.sigmoid(outputs)
        self.log("val_loss", val_loss, on_epoch=True)
        self.log_metrics(preds, y, type="val")
        return val_loss

    def test_step(self, batch, batch_idx):
        X, y = batch
        mask = X['attention_mask']
        input_ids = X['input_ids'].squeeze(1)
        outputs = self.forward(input_ids, mask)
        test_loss = self.criterion(outputs, y.float())
        preds = F.sigmoid(outputs)
        self.log("test_loss", test_loss, on_epoch=True)
        self.log_metrics(preds, y, type="test")
        return test_loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.learning_rate)
        return optimizer



if __name__ == "__main__":
    train_df = load_fdata(f"data/atomic_ood/{DATASET_TYPE}/train_{DATASET_TYPE}.csv")
    val_df = load_data("data/atomic2020_data-feb2021/dev.tsv", multi_label=True)
    test_df = load_fdata(f"data/atomic_ood/{DATASET_TYPE}/test_{DATASET_TYPE}.csv")
    train_data = DistilBERTHeadDataset(train_df, tokenizer_type=MODEL_TYPE)
    val_data = DistilBERTHeadDataset(val_df, tokenizer_type=MODEL_TYPE)
    test_data = DistilBERTHeadDataset(test_df, tokenizer_type=MODEL_TYPE)

    train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=BATCH_SIZE)
    test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE)

    emb_txt = 'frozen' if FREEZE_EMB else 'finetune'

    timestamp = get_timestamp()
    wandb_logger = WandbLogger(project="kogito-relation-matcher", name=f"distilbert_{emb_txt}_{MODEL_TYPE}_{DATASET_TYPE}")
    wandb_logger.experiment.config["epochs"] = NUM_EPOCHS
    wandb_logger.experiment.config["batch_size"] = BATCH_SIZE
    model = DistilBERTClassifier(learning_rate=LR_RATE, model_type=MODEL_TYPE, freeze_emb=FREEZE_EMB)
    trainer = pl.Trainer(default_root_dir="models/distilbert", max_epochs=NUM_EPOCHS, logger=wandb_logger, accelerator="gpu", devices=[1])
    trainer.fit(model, train_dataloaders=train_dataloader, val_dataloaders=val_dataloader)
    trainer.test(model, dataloaders=test_dataloader)
    trainer.save_checkpoint(f"models/distilbert/distilbert_model_{emb_txt}_{MODEL_TYPE}_{DATASET_TYPE}_{timestamp}.ckpt", weights_only=True)
    wandb.finish()

