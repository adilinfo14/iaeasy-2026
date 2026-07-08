import asyncio
import base64
import io

_resnet_model = None
_transform = None


def _charger_modele():
    global _resnet_model, _transform
    if _resnet_model is None:
        import torch
        from torchvision.models import ResNet18_Weights, resnet18

        weights = ResNet18_Weights.DEFAULT
        modele = resnet18(weights=weights)
        modele.eval()
        # On retire la dernière couche (classification ImageNet à 1000 classes) pour ne
        # garder que le vecteur de caractéristiques visuelles produit juste avant.
        _resnet_model = torch.nn.Sequential(*list(modele.children())[:-1])
        _transform = weights.transforms()
    return _resnet_model, _transform


def _embedding_image(modele, transform, image_path: str):
    import torch
    from PIL import Image

    image = Image.open(image_path).convert("RGB")
    tenseur = transform(image).unsqueeze(0)
    with torch.no_grad():
        vecteur = modele(tenseur).squeeze().numpy()
    return vecteur, image


def _image_vers_base64(image) -> str:
    tampon = io.BytesIO()
    image.save(tampon, format="JPEG", quality=85)
    return base64.b64encode(tampon.getvalue()).decode()


def _similarite_sync() -> dict:
    import numpy as np
    from ultralytics.utils import ASSETS

    modele, transform = _charger_modele()
    vecteur_a, image_a = _embedding_image(modele, transform, str(ASSETS / "bus.jpg"))
    vecteur_b, image_b = _embedding_image(modele, transform, str(ASSETS / "zidane.jpg"))

    produit = float(np.dot(vecteur_a, vecteur_b))
    norme_a = float(np.linalg.norm(vecteur_a))
    norme_b = float(np.linalg.norm(vecteur_b))
    similarite = produit / (norme_a * norme_b) if norme_a and norme_b else 0.0

    return {
        "type": "similarite_image",
        "image_a_base64": _image_vers_base64(image_a),
        "image_b_base64": _image_vers_base64(image_b),
        "dimension_vecteur": len(vecteur_a),
        "similarite_cosinus": round(similarite, 4),
        "explication": "Chaque image est transformée en un vecteur de nombres (un « embedding », "
        "comme pour du texte, mais ici via un réseau de neurones entraîné sur des millions de photos "
        "ImageNet) — deux images visuellement proches auraient un score élevé. Les deux photos "
        "montrent des scènes différentes (un bus urbain vs un portrait de personnes), un score modéré "
        "est donc attendu, pas un score proche de 1.",
    }


async def run_similarite() -> dict:
    return await asyncio.to_thread(_similarite_sync)
