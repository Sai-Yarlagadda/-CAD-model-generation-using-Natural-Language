from datasets import load_dataset 
from torch.utils.data import Dataset, DataLoader
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch

dataset = load_dataset("dataset location....", split="train") #load the dataset location
#dataset[0]["text"]#get caption of first image
#dataset[0]["image"]#get the corresponding first image


class ImageCaptioningDataset(Dataset):
    def __init__(self, dataset, processor):
        self.dataset = dataset
        self.processor = processor

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        encoding = self.processor(images=item["image"], text=item["text"], padding="max_length", return_tensors="pt")
        # remove batch dimension
        encoding = {k:v.squeeze() for k,v in encoding.items()}
        return encoding

def finetuning_imagecap_model(dataset, device):
    """
    Given the dataset the model finetunes and trains BLIP on the provided dataset. 
    """
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    train_dataset = ImageCaptioningDataset(dataset, processor)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=2)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    model.to(device)

    model.train()

    for epoch in range(50):
        print("Epoch:", epoch)
        for idx, batch in enumerate(train_dataloader):
            input_ids = batch.pop("input_ids").to(device)
            pixel_values = batch.pop("pixel_values").to(device)

            outputs = model(input_ids=input_ids,
                            pixel_values=pixel_values,
                            labels=input_ids)
            
            loss = outputs.loss
            print("Loss:", loss.item())
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

def Inferencing_image_captioning_model(model, image, device, processor):

    """
    Performing inferencing on the image and this function returns a caption to the image
    """
    inputs = processor(images=image, return_tensors="pt").to(device)
    pixel_values = inputs.pixel_values

    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return generated_caption

if __name__ == '__main__':

    finetuning_imagecap_model('dataset_location')
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
