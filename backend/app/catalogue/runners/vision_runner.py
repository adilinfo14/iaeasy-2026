import asyncio
import base64
import io

_yolo_models: dict[str, object] = {}
_yolo_cls_models: dict[str, object] = {}


def _sample_image_path() -> str:
    from ultralytics.utils import ASSETS

    return str(ASSETS / "bus.jpg")


def _image_to_base64(annotated_bgr) -> str:
    from PIL import Image

    annotated_rgb = annotated_bgr[:, :, ::-1]
    img = Image.fromarray(annotated_rgb)
    tampon = io.BytesIO()
    img.save(tampon, format="JPEG", quality=85)
    return base64.b64encode(tampon.getvalue()).decode()


def _detect_sync(model_ref: str) -> dict:
    if model_ref not in _yolo_models:
        from ultralytics import YOLO

        _yolo_models[model_ref] = YOLO(model_ref)

    image_path = _sample_image_path()
    results = _yolo_models[model_ref](image_path, verbose=False)[0]

    detections = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        detections.append(
            {
                "etiquette": results.names[cls_id],
                "confiance": round(float(box.conf[0]), 3),
                "boite": [round(float(v), 1) for v in box.xyxy[0].tolist()],
            }
        )

    return {
        "type": "detection_objets",
        "image_annotee_base64": _image_to_base64(results.plot()),
        "objets_detectes": detections,
        "nb_objets": len(detections),
        "note": "Image d'exemple générique fournie par l'outil — remplaçable par une vraie photo aérienne.",
    }


def _classify_sync(model_ref: str) -> dict:
    if model_ref not in _yolo_cls_models:
        from ultralytics import YOLO

        _yolo_cls_models[model_ref] = YOLO(model_ref)

    image_path = _sample_image_path()
    results = _yolo_cls_models[model_ref](image_path, verbose=False)[0]

    top5_idx = results.probs.top5
    top5_conf = results.probs.top5conf.tolist()
    predictions = [
        {"etiquette": results.names[i], "confiance": round(float(c), 4)}
        for i, c in zip(top5_idx, top5_conf)
    ]

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    return {
        "type": "classification_image",
        "image_base64": image_b64,
        "predictions": predictions,
        "note": "Image d'exemple générique (modèle entraîné sur ImageNet, non spécialisé agriculture).",
    }


async def run_detection(model_ref: str) -> dict:
    return await asyncio.to_thread(_detect_sync, model_ref)


async def run_classification(model_ref: str) -> dict:
    return await asyncio.to_thread(_classify_sync, model_ref)
