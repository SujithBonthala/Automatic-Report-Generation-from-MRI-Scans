from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import tensorflow as tf
from tensorflow import keras
import cv2
import matplotlib.pyplot as plt
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, input_ids):
        self.input_ids = input_ids["input_ids"]

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            "input_ids": self.input_ids[idx],
            "labels": self.input_ids[idx],
        }

def baggingClassificationTumor(img, model1, model2):
    labels=["Glioma Tumor", "Meningioma Tumor", "Normal", "Pituitary Tumor"]
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32')
    img /= 255.0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((1, 224, 224, 3))
    prediction1 = model1.predict(img, verbose=0)
    prediction2 = model2.predict(img, verbose=0)
    prediction_list1 = prediction1[0].tolist()
    for label in range(len(prediction_list1)):
        prediction_list1[label] = float(prediction_list1[label])*100
    prediction_list2 = prediction2[0].tolist()
    for label in range(len(prediction_list2)):
        prediction_list2[label] = float(prediction_list2[label])*100
    predictions = []
    for idx in range(len(prediction_list1)):
        predictions.append(prediction_list1[idx]+prediction_list2[idx])
    labels_predictions = zip(labels, predictions)
    sorted_predictions = sorted(labels_predictions, reverse = True, key = lambda x : x[1])
    return sorted_predictions[0][0]

def baggingClassificationAlzheimer(img, model1, model2):
    labels=["Mildly demented", "Moderately demented", "Non demented", "Very mildly demented"]
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32')
    img /= 255.0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((1, 224, 224, 3))
    prediction1 = model1.predict(img, verbose=0)
    prediction2 = model2.predict(img, verbose=0)
    prediction_list1 = prediction1[0].tolist()
    for label in range(len(prediction_list1)):
        prediction_list1[label] = float(prediction_list1[label])*100
    prediction_list2 = prediction2[0].tolist()
    for label in range(len(prediction_list2)):
        prediction_list2[label] = float(prediction_list2[label])*100
    predictions = []
    for idx in range(len(prediction_list1)):
        predictions.append(prediction_list1[idx]+prediction_list2[idx])
    labels_predictions = zip(labels, predictions)
    sorted_predictions = sorted(labels_predictions, reverse = True, key = lambda x : x[1])
    return sorted_predictions[0][0]

def baggingClassificationStroke(img, model1, model2):
    labels=["Stroke", "No Stroke"]
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((1, 224, 224, 3))
    prediction1 = model1.predict(img, verbose=0)
    prediction2 = model2.predict(img, verbose=0)
    if((prediction1[0][0] + prediction2[0][0]) / 2 >= 0.5):
        return "Stroke"
    else:
        return "No Stroke"
    
def getReport(report):
    idx = report.find("Report:")
    return report[idx+8:]

def generateReport(label1, label2, label3):
    if label1 == 'absent':
        model_tumor = GPT2LMHeadModel.from_pretrained("./models/model_cpu_tumor_normal")
        tokenizer_tumor = GPT2Tokenizer.from_pretrained("./models/tokenizer_tumor_normal")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_tumor.to(device)
        input_text = f"Diagnosis: {label1}. Report:"
        input_ids = tokenizer_tumor.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_tumor.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_tumor = tokenizer_tumor.decode(generated_text[0], skip_special_tokens=True)
    elif label1 == 'men':
        model_tumor = GPT2LMHeadModel.from_pretrained("./models/model_cpu_tumor_meningioma")
        tokenizer_tumor = GPT2Tokenizer.from_pretrained("./models/tokenizer_tumor_meningioma")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_tumor.to(device)
        input_text = f"Diagnosis: {label1}. Report:"
        input_ids = tokenizer_tumor.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_tumor.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_tumor = tokenizer_tumor.decode(generated_text[0], skip_special_tokens=True)
    elif label1 == 'glue':
        model_tumor = GPT2LMHeadModel.from_pretrained("./models/model_cpu_tumor_glioma")
        tokenizer_tumor = GPT2Tokenizer.from_pretrained("./models/tokenizer_tumor_glioma")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_tumor.to(device)
        input_text = f"Diagnosis: {label1}. Report:"
        input_ids = tokenizer_tumor.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_tumor.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_tumor = tokenizer_tumor.decode(generated_text[0], skip_special_tokens=True)
    else:
        model_tumor = GPT2LMHeadModel.from_pretrained("./models/model_cpu_tumor_pituitary")
        tokenizer_tumor = GPT2Tokenizer.from_pretrained("./models/tokenizer_tumor_pituitary")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_tumor.to(device)
        input_text = f"Diagnosis: {label1}. Report:"
        input_ids = tokenizer_tumor.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_tumor.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_tumor = tokenizer_tumor.decode(generated_text[0], skip_special_tokens=True)

    if label2 == 'no dementia':
        model_alzheimer = GPT2LMHeadModel.from_pretrained("./models/model_cpu_alzheimer_normal")
        tokenizer_alzheimer = GPT2Tokenizer.from_pretrained("./models/tokenizer_alzheimer_normal")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_alzheimer.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_alzheimer.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_alzheimer.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_alzheimer = tokenizer_alzheimer.decode(generated_text[0], skip_special_tokens=True)
    elif label2 == 'very mildly demented':
        model_alzheimer = GPT2LMHeadModel.from_pretrained("./models/model_cpu_alzheimer_very")
        tokenizer_alzheimer = GPT2Tokenizer.from_pretrained("./models/tokenizer_alzheimer_very")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_alzheimer.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_alzheimer.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_alzheimer.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_alzheimer = tokenizer_alzheimer.decode(generated_text[0], skip_special_tokens=True)
    elif label2 == 'mildly demented':
        model_alzheimer = GPT2LMHeadModel.from_pretrained("./models/model_cpu_alzheimer_mild")
        tokenizer_alzheimer = GPT2Tokenizer.from_pretrained("./models/tokenizer_alzheimer_mild")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_alzheimer.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_alzheimer.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_alzheimer.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_alzheimer = tokenizer_alzheimer.decode(generated_text[0], skip_special_tokens=True)
    else:
        model_alzheimer = GPT2LMHeadModel.from_pretrained("./models/model_cpu_alzheimer_moderate")
        tokenizer_alzheimer = GPT2Tokenizer.from_pretrained("./models/tokenizer_alzheimer_moderate")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_alzheimer.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_alzheimer.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_alzheimer.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_alzheimer = tokenizer_alzheimer.decode(generated_text[0], skip_special_tokens=True)

    if label3 == 'normal':
        model_stroke = GPT2LMHeadModel.from_pretrained("./models/model_cpu_stroke_absent")
        tokenizer_stroke = GPT2Tokenizer.from_pretrained("./models/tokenizer_stroke_absent")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_stroke.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_stroke.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_stroke.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_stroke = tokenizer_stroke.decode(generated_text[0], skip_special_tokens=True)
    else:
        model_stroke = GPT2LMHeadModel.from_pretrained("./models/model_cpu_stroke_present")
        tokenizer_stroke = GPT2Tokenizer.from_pretrained("./models/tokenizer_stroke_present")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_stroke.to(device)
        input_text = f"Diagnosis: {label2}. Report:"
        input_ids = tokenizer_stroke.encode(input_text, return_tensors="pt", padding=True, max_length=128, truncation=True).to(device)
        generated_text = model_stroke.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, top_k=20)
        generated_report_stroke = tokenizer_stroke.decode(generated_text[0], skip_special_tokens=True)
    
    return getReport(generated_report_tumor)+" "+getReport(generated_report_alzheimer)+" "+getReport(generated_report_stroke)

@app.route('/genreport', methods = ['GET'])
def process_img():
    try:
        img_path = request.args.get('pathName')
        img = plt.imread(img_path)
        
        densenet_tumor = tf.keras.models.load_model('./models/best_weights_densenet_tumor.h5')
        xceptionnet_tumor = tf.keras.models.load_model('./models/best_weights_xceptionnet_tumor.h5')
        tumor_label = baggingClassificationTumor(img, densenet_tumor, xceptionnet_tumor)
        del densenet_tumor
        del xceptionnet_tumor

        densenet_alzheimer = tf.keras.models.load_model('./models/best_weights_densenet_alzheimer.h5')
        resnet_alzheimer = tf.keras.models.load_model('./models/best_weights_resnet_alzheimer.h5')
        alzheimer_label = baggingClassificationAlzheimer(img, densenet_alzheimer, resnet_alzheimer)
        del densenet_alzheimer
        del resnet_alzheimer

        densenet_stroke = tf.keras.models.load_model('./models/best_weights_densenet_stroke.h5')
        resnet_stroke = tf.keras.models.load_model('./models/best_weights_resnet_stroke.h5')
        stroke_label = baggingClassificationStroke(img, densenet_stroke, resnet_stroke)
        del densenet_stroke
        del resnet_stroke

        torch.cuda.empty_cache()
        labels_dict = {'Meningioma Tumor': 'men', 'Glioma Tumor': 'glue', 'Pituitary Tumor': 'pit',
                    'Normal': 'absent', 'Mildly demented': 'mildly demented',  'Moderately demented':
                    'moderately demented', 'Non demented': 'no dementia', 'Very mildly demented':
                    'very mildly demented', 'No Stroke': 'normal', 'Stroke': 'stroke'}
        report = generateReport(labels_dict[tumor_label], labels_dict[alzheimer_label], labels_dict[stroke_label])
        print(report)
    except Exception as e:
        return jsonify({
			"message": "Failure",
			"data": e
		})
    else:
        return jsonify({
			"message": "Success",
			"data": report
		})

print("Flask Server is running on port 6565")
if __name__ == '__main__':
	app.run(debug=False, port=6565)