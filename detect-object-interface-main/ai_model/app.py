from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from process_video import *
from utils import allowed_file
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from services.llm_service import generate_summary

load_dotenv()

app = Flask(__name__)
CORS(app)

# ================= CONFIG =================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ✅ CHANGED: output-images instead of output-videos
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'output-images')
INPUT_FOLDER = os.path.join(BASE_DIR, 'test-inputs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['INPUT_VIDEOS_FOLDER'] = INPUT_FOLDER
app.config['INPUT_VIDEO_PATH'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= DB MODELS =================

class UserInputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_video_name = db.Column(db.String(50))
    confidence_input = db.Column(db.DECIMAL(5, 4))
    iou_input = db.Column(db.DECIMAL(5, 4))


class Detections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frame_number = db.Column(db.Integer)
    box_left = db.Column(db.Integer)
    box_top = db.Column(db.Integer)
    box_width = db.Column(db.Integer)
    box_height = db.Column(db.Integer)
    class_name = db.Column(db.String(20))
    confidence = db.Column(db.DECIMAL(10, 9))
    user_input_id = db.Column(db.Integer)


with app.app_context():
    db.create_all()

# ================= DB FUNCTIONS =================

def save_user_input(video_name, confidence, iou):
    new_input = UserInputs(
        server_video_name=video_name,
        confidence_input=confidence,
        iou_input=iou
    )
    db.session.add(new_input)
    db.session.commit()
    return new_input.id


def save_all_detections(detections, user_input_id):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()

    objs = []
    for d in detections:
        objs.append(Detections(
            frame_number=d['frame_number'],
            box_left=d['box']['left'],
            box_top=d['box']['top'],
            box_width=d['box']['width'],
            box_height=d['box']['height'],
            class_name=d['class_name'],
            confidence=d['confidence'],
            user_input_id=user_input_id
        ))

    session.bulk_save_objects(objs)
    session.commit()

# ================= ROUTES =================

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files.get('video')
    if not file:
        return jsonify({'error': 'no video'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['INPUT_VIDEOS_FOLDER'], filename)

    os.makedirs(app.config['INPUT_VIDEOS_FOLDER'], exist_ok=True)
    file.save(path)

    app.config['INPUT_VIDEO_PATH'] = path

    return jsonify({'message': 'uploaded successfully'})


@app.route("/detect", methods=['POST'])
def detect():
    try:
        data = request.get_json()

        confidence = float(data.get('confidence', 0.5))
        iou = float(data.get('iou', 0.5))

        video_path = app.config['INPUT_VIDEO_PATH']

        detections_list = DetectionsProcess()

        processor = VideoProcessor(
            detections_list,
            video_path,
            confidence,
            iou
        )

        # ✅ returns IMAGE filename now (.jpg)
        output_image = processor.main_process()

        user_id = save_user_input(output_image, confidence, iou)
        save_all_detections(detections_list.all_detections, user_id)

        return jsonify({
            "message": "processing done",
            "output_video": output_image  # keep same key (frontend uses it)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ UPDATED: Serve image instead of video
@app.route("/result/<name>")
def result(name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)

    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404

    return send_file(file_path, mimetype='image/jpeg')


@app.route("/detections", methods=['GET'])
def get_detections():
    data = Detections.query.order_by(Detections.id.desc()).limit(10).all()

    return jsonify([
        {
            "frame": d.frame_number,
            "class": d.class_name,
            "confidence": float(d.confidence)
        } for d in data
    ])


@app.route("/analyze", methods=["GET"])
def analyze():
    try:
        detections = Detections.query.all()

        detections_list = [
            {"frame": d.frame_number, "confidence": float(d.confidence)}
            for d in detections
        ]

        summary = generate_summary(detections_list)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return {"message": "Backend is running 🚀"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)