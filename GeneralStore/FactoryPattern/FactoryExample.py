import MRIPreproc
import object_factory


class MRIServiceBuilder:
    def __init__(self):
        self._instance = None

    # this code ensures that we only call this once
    def __call__(self, plan, image_file_path, subject_id, runx, table_name, **_ignored):
        if not self._instance:
            self.prepare(plan, image_file_path, subject_id, runx, table_name)
        return self._instance

    def prepare(self, plan, image_file_path, subject_id, runx, table_name):
        print("EXAPlan = ", plan)

        if plan == "adni-kim":
            self._instance = MRIPreproc.KIM_MRI_Preproc(
                image_file_path, subject_id, runx, table_name
            )
        elif plan == "AMP":
            self._instance = MRIPreproc.AMP_MRI_Preproc(
                image_file_path, subject_id, runx, table_name
            )


class EXBPreproc:
    def __init__(self, image_file_path):
        self._image_file_path = image_file_path

    def test_connection(self):
        print(f"Preparing EXB {self._image_file_path} for preprocessing")


class EXBServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, plan, image_file_path, **_ignored):
        if not self._instance:
            roadmap = self.prepare(plan)
            self._instance = EXBPreproc(image_file_path)
        return self._instance

    def prepare(self, plan):
        print("EXB Plan = ", plan)
        return plan


class EXCPreproc:
    def __init__(self, image_file_path):
        self._image_file_path = image_file_path

    def test_connection(self):
        print(f"Preparing MRI+ EXB {self._image_file_path} for preprocessing")


class EXCServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, plan, image_file_path, **_ignored):
        if not self._instance:
            roadmap = self.prepare(plan)
            self._instance = EXCPreproc(image_file_path)
        return self._instance

    def prepare(self, plan):
        print("EXA+ EXB Plan = ", plan)
        return plan


class ModalityServiceProvider(object_factory.ObjectFactory):
    def get(self, service_id, **kwargs):
        return self.create(service_id, **kwargs)


services = ModalityServiceProvider()
services.register_builder("MRI", MRIServiceBuilder())
services.register_builder("EXB", EXBServiceBuilder())
services.register_builder("EXC", EXCServiceBuilder())
