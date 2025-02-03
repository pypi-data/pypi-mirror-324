from langchain.schema import HumanMessage

class ImageMessageBuilder:
    def __init__(self):
        self.content = []

    def add_text(self, text: str) -> "ImageMessageBuilder":
        """
        텍스트 내용을 추가합니다.
        """
        self.content.append({"type": "text", "text": text})
        return self

    def add_image_from_base64(self, image_data: str, image_format: str = "png") -> "ImageMessageBuilder":
        """
        Base64로 인코딩된 이미지 데이터를 추가합니다.
        """
        image_url = f"data:image/{image_format};base64,{image_data}"
        self.content.append({"type": "image_url", "image_url": {"url": image_url}})
        return self

    def build(self) -> HumanMessage:
        """
        HumanMessage 객체를 생성합니다.
        """
        return HumanMessage(content=self.content)