import cv2
import matplotlib.cm
import torch

CLASS_NAMES = ("ign", "ped", "peo", "byc", "car", "van", "trk", "tcy", "atc", "bus", "mtr", "oth")


def visualize(img, annos, classnames=CLASS_NAMES):
    """
    Mark annotation bounding box on the image.
    :param img: cv2 image
    :param annos: array with annotations
    :param classnames: class name text
    :return: marked image
    """
    img = img.copy()
    font = cv2.FONT_HERSHEY_DUPLEX
    colors = load_colors()
    for anno in annos:
        if not isinstance(anno, torch.Tensor):
            anno = anno.strip().split(',')
        x, y, w, h, score, cls = \
            int(anno[0]), int(anno[1]), int(anno[2]), int(anno[3]), anno[4], anno[5]
        cv2.rectangle(img, (x, y), (x + w, y + h), colors[int(cls)], 1)

    for i in range(len(classnames)):
        cv2.rectangle(img, (i * 35, 0), ((i+1) * 35, 15), colors[i], thickness=-1)
        cv2.putText(img, classnames[i], (i * 35 + 5, 13), font, 0.4, (255, 255, 255), 1, False)

    return img


def visualize_ctnet(img, annos, classnames=CLASS_NAMES):
    """
    Mark annotation bounding box on the image.
    :param img: cv2 image
    :param annos: array with annotations
    :param classnames: class name text
    :return: marked image
    """
    img = img.copy()
    font = cv2.FONT_HERSHEY_DUPLEX
    colors = load_colors()
    for anno in annos:
        if not isinstance(anno, torch.Tensor):
            anno = anno.strip().split(',')
            x, y, w, h, score, cls = \
                int(anno[0]), int(anno[1]), int(anno[2]), int(anno[3]), anno[4], anno[5]
        else:
            x, y, w, h, score, cls = \
                int(anno[0]), int(anno[1]), int(anno[2]), int(anno[3]), anno[4], anno[5] + 1
        cv2.rectangle(img, (x, y), (x + w, y + h), colors[int(cls)], 1)

    for i in range(len(classnames)):
        cv2.rectangle(img, (i * 35, 0), ((i+1) * 35, 15), colors[i], thickness=-1)
        cv2.putText(img, classnames[i], (i * 35 + 5, 13), font, 0.4, (255, 255, 255), 1, False)

    return img



def load_colors(num=12):
    """
    Generate color maps.
    :param num: color numbers.
    :return: colors, RGB from 0 to 255
    """
    colors = matplotlib.cm.get_cmap('tab20').colors
    assert num < len(colors)
    colors = [(int(color[0]*255), int(color[1]*255), int(color[2]*255)) for color in colors]
    return colors[:num]


if __name__ == '__main__':
    dev_img = cv2.imread('../../data/test/images/9999936_00000_d_0000070.jpg')
    with open('../../../40000/9999936_00000_d_0000070.txt', 'r') as reader:
        dev_annos = reader.readlines()
    marked_img = visualize(dev_img, dev_annos)
    cv2.imwrite('../../../vis_demo.jpg', marked_img)
    cv2.waitKey(0)
