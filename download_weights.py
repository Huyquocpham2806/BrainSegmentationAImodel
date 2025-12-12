import gdown

url = "https://drive.google.com/drive/folders/1bllUnILulSeENQWfHC_j9W-ngWqBxtGj?hl=vi"
gdown.download(url, "weights/best_model.pth", quiet=False)
