# instantiate the model
from pyannote.audio import Model
model = Model.from_pretrained(
  "pyannote/segmentation-3.0", 
  use_auth_token="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")
