# The factory pattern example starts here, simply uncomment the config of interest and run with
# > python main.py
import FactoryExample

# config = {
#     'plan': 'Test Y',
#     'modality': 'PET',
#     'image_file_path': 'U:\PET+MR+AI\SampleData\Sample2\SamplePET+MRSet\ADNI\129_S_4369\_3D_6x300s_4i_16s__FDG\2013-11-21_09_31_00.0\I399166\ADNI_129_S_4369_PET.v1'
# }

# config = {
# 'plan': 'Test Z',
# 'modality': 'MRI',
# 'image_file_path': 'U:\PET+MR+AI\SampleData\Sample2\SamplePET+MRSet\ADNI\129_S_4369\_3D_6x300s_4i_16s__FDG\2013-11-21_09_31_00.0\I399166\ADNI_129_S_4369_MRI.v2'
# }

config = {"plan": "Test B", "modality": "MRIPET", "image_file_path": "ThisIsOnlyATest"}

pipeline = FactoryExample.services.get(config["modality"], **config)
pipeline.test_connection()
