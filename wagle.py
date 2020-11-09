import logging
import dataset
import evaluate
import predict
import gen_anchors
import train
import argparse
import testcase
import utils.multi_gpu_model


class WagleDensityYolo():
    def __init__(self):
        logging.disable(logging.WARNING)
        args = self.parse_args()

        testcase.yolo_argument_exit('fail') if args.mode is None \
            else testcase.yolo_argument_exit('pass')

        #
        utils.multi_gpu_model.gpu_initialize()
        self.mode_select(args)

    def parse_args(self):
        argparser = argparse.ArgumentParser(
            description='Integrated application for estimating human density'
        )
        argparser.add_argument('--mode',
                               choices=['train', 'gen_anchors', 'predict',
                                        'evaluate', 'dataset'])
        argparser.add_argument('-a', '--anchors',
                               help='number of anchors to use')
        argparser.add_argument('-c', '--conf',
                               help='path to configuration file')
        argparser.add_argument('--host',
                               help='IP address that means server')
        argparser.add_argument(
            '-i',
            '--input',
            help='path to an image, a directory of images, a video, or webcam')
        argparser.add_argument('-m', '--mot', default=False,
                               help='path to a mot format gt file')
        argparser.add_argument('-o', '--output',
                               default='output/',
                               help='path to output directory')
        argparser.add_argument('-p', '--path',
                               help='path to a directory of images')
        argparser.add_argument('-t', '--train',
                               help='path to a train directory')
        argparser.add_argument('-v', '--valid',
                               help='path to a valid directory')
        args = argparser.parse_args()
        return args

    @staticmethod
    def mode_select(args):
        if args.mode == 'train':
            train.train_main_(args)
        elif args.mode == 'gen_anchors':
            gen_anchors.anchor_main_(args)
        elif args.mode == 'predict':
            predict.predict_main_(args)
        elif args.mode == 'evaluate':
            evaluate.evaluate_main_(args)
        elif args.mode == 'dataset':
            dataset.dataset_main_(args)
        else:
            testcase.yolo_argument_exit('fail')


if __name__ == '__main__':
    dy = WagleDensityYolo()

