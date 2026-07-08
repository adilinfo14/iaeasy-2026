import asyncio
import base64
import io


def _generer_image_document():
    from PIL import Image, ImageDraw, ImageFont

    largeur, hauteur = 640, 240
    image = Image.new("RGB", (largeur, hauteur), color="white")
    dessin = ImageDraw.Draw(image)

    police = None
    for chemin_police in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            police = ImageFont.truetype(chemin_police, 30)
            break
        except OSError:
            continue
    if police is None:
        police = ImageFont.load_default()

    lignes = [
        "FACTURE N° 2847",
        "Montant TTC : 1233,00 EUR",
        "Echeance : 15/09/2026",
    ]
    y = 30
    for ligne in lignes:
        dessin.text((30, y), ligne, fill="black", font=police)
        y += 65

    return image


def _image_vers_base64(image) -> str:
    tampon = io.BytesIO()
    image.save(tampon, format="PNG")
    return base64.b64encode(tampon.getvalue()).decode()


def _ocr_sync() -> dict:
    import pytesseract

    image = _generer_image_document()
    texte_extrait = pytesseract.image_to_string(image, lang="fra")

    return {
        "type": "ocr_texte",
        "image_base64": _image_vers_base64(image),
        "texte_extrait": texte_extrait.strip(),
        "note": "Image de facture générée à la volée (pas une vraie photo) pour un test 100% "
        "reproductible sans dépendre d'un fichier externe — remplaçable par une vraie photo de "
        "document scanné, avec une fiabilité qui dépend alors fortement de la netteté et de l'angle.",
    }


async def run_ocr() -> dict:
    return await asyncio.to_thread(_ocr_sync)
