import asyncio

_yolo_model = None


def _sample_image_path() -> str:
    from ultralytics.utils import ASSETS

    return str(ASSETS / "bus.jpg")


def _detect_sync(model_ref: str) -> dict:
    global _yolo_model
    if _yolo_model is None:
        from ultralytics import YOLO

        _yolo_model = YOLO(model_ref)

    image_path = _sample_image_path()
    results = _yolo_model(image_path, verbose=False)[0]

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
        "image_analysee": "image d'exemple fournie par l'outil (photo générique — remplaçable par une vraie photo aérienne)",
        "objets_detectes": detections,
        "nb_objets": len(detections),
    }


async def run_detection(model_ref: str) -> dict:
    return await asyncio.to_thread(_detect_sync, model_ref)
