# Mistral.AI Models

**pip install -r requirements.txt**

```
1. Run ./src/get_data_from_db.ipynb - to extract original documents from MongoDB
2. Run python ./src/upload_in_storage.py - to upload this original data in Vector Storage
3. Run python ask.py "question" - to ask question based on the information that was uploaded in Vector Storage

Additionally: 
Run ./src/upload_to_db.ipynb - to upload original documents to MongoDB
```