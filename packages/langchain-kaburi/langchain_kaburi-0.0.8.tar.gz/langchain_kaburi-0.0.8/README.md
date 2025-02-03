# 랭체인 편의 기능 라이브러리

**Builders**
```
from langchain_kaburi.builders import ImageMessageBuilder

img_builder = ImageMessageBuilder()
message = (
    img_builder.add_text("텍스트로 변환해")
    .add_image_from_base64(image_data)
    .build()
)
```