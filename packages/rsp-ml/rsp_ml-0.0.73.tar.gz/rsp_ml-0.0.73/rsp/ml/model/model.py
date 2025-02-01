import requests
import torch
import torch.jit
from enum import Enum
import huggingface_hub

class MODELS(Enum):
    TUCARC3D = 'TUC-AR-C3D'

class WEIGHTS(Enum):
    TUCAR = 'tuc-ar.pth'
    UCF101 = 'ufc101.pth'

#__example__ #import rsp.ml.model as model
#__example__
#__example__ action_recognition_model = model.load_model(MODEL.TUCARC3D, WEIGHTS.TUCAR)
def load_model(
        model:MODELS,
        weights:WEIGHTS
    ):
    """
    Loads a pretrained PyTorch model from HuggingFace.

    Parameters
    ----------
    model : MODEL
        ID of the model
    weights : WEIGHTS
        ID of the weights

    Returns
    -------
    torch.nn.Module
        Pretrained PyTorch model
    """
    api = huggingface_hub.HfApi()
    model_path = api.hf_hub_download(f'SchulzR97/{model.value}', filename=weights.value)

    model = torch.jit.load(model_path)

    return model

#__example__ #import rsp.ml.model as model
#__example__
#__example__ model_weight_files = model.list_model_weights()
def list_model_weights():
    """
    Lists all available weight files.

    Returns
    -------
    List[Tuple(str, str)]
        List of (MODEL:str, WEIGHT:str)
    """
    weight_files = []
    username = 'SchulzR97'
    for model in huggingface_hub.list_models(author=username):
        for file in huggingface_hub.list_repo_files(model.id):
            appendix = file.split('.')[-1]
            if appendix not in ['bin', 'pt', 'pth']:
                continue
            model_id = model.id.replace(f'{username}/', '')
            weight_id = file
            weight_files.append((model_id, weight_id))
            print(weight_files[-1])
    return weight_files

if __name__ == '__main__':
    list_model_weights()

    model = load_model(MODELS.TUCARC3D, WEIGHTS.TUCAR)