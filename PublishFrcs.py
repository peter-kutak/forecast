from Publish import Publish

class PublishFrcs(Publish):
  def __init__(self):
    super().__init__("forecast")
    self.msgPattern=("[{{ "
            "\"bn\": \"myhome/forecast/\""
            ",\"bt\": {}"
            "}},{{"
            "\"n\": \"temp\","
            "\"v\": {},"
            "\"u\": \"degC\""
            "}}]")


  def publish(self, temp):
    super().publish(temp)


