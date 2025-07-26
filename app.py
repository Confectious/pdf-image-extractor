from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import base64

app = FastAPI()

@app.post("/extract-images/")
async def extract_images(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    images_data = []

    for page_num in range(min(2, len(doc))):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            b64_img = base64.b64encode(image_bytes).decode("utf-8")

            images_data.append({
                "page": page_num,
                "index": img_index,
                "extension": ext,
                "base64": b64_img
            })

    return JSONResponse(content={"images": images_data})
