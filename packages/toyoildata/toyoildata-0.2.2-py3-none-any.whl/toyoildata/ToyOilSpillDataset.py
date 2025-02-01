import torch
import numpy as np
from torch.utils.data import Dataset
from toyoildata.utils import gen_lab_pred_pair, gen_sar_like_image, overlap_grid
import cv2


class ToyOilSpillDataset(Dataset):
    def __init__(
        self,
        resolution=256,
        tp=4,
        fp=1,
        fn=1,
        num=64,
        confidence_range=(0.6, 1.0),
        pred_blur=1,
        size_range=(1, 16),
    ):
        self.resolution = resolution
        self.tp = tp
        self.fp = fp
        self.fn = fn
        self.num = num
        self.confidence_range = confidence_range
        self.pred_blur = pred_blur
        self.size_range = size_range

    def _gen_lab_pred_pair(self):
        confidences = np.random.uniform(*self.confidence_range, self.tp + self.fp)
        return gen_lab_pred_pair(
            tp=self.tp,
            fp=self.fp,
            fn=self.fn,
            resolution=self.resolution,
            confidences=confidences,
            size_range=self.size_range,
        )

    def __len__(self):
        return self.num

    def __getitem__(self, idx):
        pred, label = self._gen_lab_pred_pair()
        label = torch.tensor(label)
        pred = torch.tensor(pred)
        if self.pred_blur > 0:
            pred = pred.numpy()
            sides = int(self.pred_blur * 2)
            ## make sure sides are odd
            sides = sides + 1 if sides % 2 == 0 else sides
            pred = cv2.GaussianBlur(
                pred, (self.pred_blur, self.pred_blur), self.pred_blur
            )
            pred = torch.tensor(pred)
        img = torch.tensor(gen_sar_like_image(label))
        return img, pred, label

    def show_examples(self):
        ds = repr(self)
        print(f"Showing examples from {ds}")
        imgs, preds, labs = zip(*[self[i] for i in range(16)])
        preds_hard = [1.0 * (p > 0.5) for p in preds]
        overlap_grid(
            labs,
            preds_hard,
            imgs,
            title=f"Examples with tp: {self.tp}, fp: {self.fp}, fn: {self.fn}",
        )

    def __repr__(self):
        return f"ToyOilSpillDataset(resolution={self.resolution}, tp={self.tp}, fp={self.fp}, fn={self.fn}, confidence_range={self.confidence_range}, num={self.num}, pred_blur={self.pred_blur})"


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    ds = ToyOilSpillDataset()
    ds.show_examples()
    plt.show()
