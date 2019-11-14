import tensorflow as tf
import numpy as np
import sys


def setup_tf():
    """
    initialize tensorflow
    """
    sess = tf.Session()  # TF session

    saver = tf.train.Saver(max_to_keep=1)  # saver saves model to file
    model_dir = 'model/'
    latest_snapshot = tf.train.latest_checkpoint(model_dir)  # is there a saved model?

    # load saved model if available
    print('Init with stored values from ' + latest_snapshot)
    saver.restore(sess, latest_snapshot)

    return sess, saver


# TODO Geen idee wat deze types zijn, uitzoeken wat het zijn en de beste kiezen.
class DecoderType:
    BestPath = 0
    # BeamSearch = 1
    # WordBeamSearch = 2


class Model:
    """
    minimalistic TF model for HTR
    """

    # TODO kijken of hier iets mee gedaan kan/moet worden (stond al hardcoded in het orgineel)
    img_size = (128, 32)
    max_text_length = 32

    def __init__(self, char_list):
        """
        init model: add CNN, RNN and CTC and initialize TF
        """
        self.char_list = char_list

        # input image batch
        self.input_image = tf.placeholder(tf.float32, shape=(None, Model.img_size[0], Model.img_size[1]))

        # setup CNN, RNN and CTC
        # TODO gebruiken we al deze dingen? Kijken of dingen weg kunnen op basis van wat we gebruiken.
        self.setup_cnn()
        self.setup_rnn()
        self.setup_ctc()

        # initialize TF
        (self.sess, self.saver) = setup_tf()

    def setup_cnn(self):
        """
        create CNN layers and return output of these layers
        """
        cnnIn4d = tf.expand_dims(input=self.input_image, axis=3)

        # list of parameters for the layers
        kernelVals = [5, 5, 3, 3, 3]
        featureVals = [1, 32, 64, 128, 128, 256]
        strideVals = poolVals = [(2, 2), (2, 2), (1, 2), (1, 2), (1, 2)]
        numLayers = len(strideVals)

        # create layers
        pool = cnnIn4d  # input to first CNN layer
        for i in range(numLayers):
            kernel = tf.Variable(
                tf.truncated_normal([kernelVals[i], kernelVals[i], featureVals[i], featureVals[i + 1]], stddev=0.1))
            conv = tf.nn.conv2d(pool, kernel, padding='SAME', strides=(1, 1, 1, 1))
            conv_norm = tf.layers.batch_normalization(conv)
            relu = tf.nn.relu(conv_norm)
            pool = tf.nn.max_pool(relu, (1, poolVals[i][0], poolVals[i][1], 1),
                                  (1, strideVals[i][0], strideVals[i][1], 1), 'VALID')

        self.cnnOut4d = pool

    def setup_rnn(self):
        """
        create RNN layers and return output of these layers
        """
        rnnIn3d = tf.squeeze(self.cnnOut4d, axis=[2])

        # basic cells which is used to build RNN
        numHidden = 256
        cells = [tf.contrib.rnn.LSTMCell(num_units=numHidden, state_is_tuple=True) for _ in range(2)]  # 2 layers

        # stack basic cells
        stacked = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        # bidirectional RNN
        # BxTxF -> BxTx2H
        ((fw, bw), _) = tf.nn.bidirectional_dynamic_rnn(cell_fw=stacked, cell_bw=stacked, inputs=rnnIn3d,
                                                        dtype=rnnIn3d.dtype)

        # BxTxH + BxTxH -> BxTx2H -> BxTx1X2H
        concat = tf.expand_dims(tf.concat([fw, bw], 2), 2)

        # project output to chars (including blank): BxTx1x2H -> BxTx1xC -> BxTxC
        kernel = tf.Variable(tf.truncated_normal([1, 1, numHidden * 2, len(self.char_list) + 1], stddev=0.1))
        self.rnnOut3d = tf.squeeze(tf.nn.atrous_conv2d(value=concat, filters=kernel, rate=1, padding='SAME'), axis=[2])

    def setup_ctc(self):
        """
        create CTC loss and decoder and return them
        """
        # BxTxC -> TxBxC
        self.ctcIn3dTBC = tf.transpose(self.rnnOut3d, [1, 0, 2])
        # ground truth text as sparse tensor
        self.gtTexts = tf.SparseTensor(tf.placeholder(tf.int64, shape=[None, 2]), tf.placeholder(tf.int32, [None]),
                                       tf.placeholder(tf.int64, [2]))

        # calc loss for batch
        self.seqLen = tf.placeholder(tf.int32, [None])
        self.loss = tf.reduce_mean(
            tf.nn.ctc_loss(labels=self.gtTexts, inputs=self.ctcIn3dTBC, sequence_length=self.seqLen,
                           ctc_merge_repeated=True))

        # calc loss for each element to compute label probability
        self.savedCtcInput = tf.placeholder(tf.float32, shape=[Model.max_text_length, None, len(self.char_list) + 1])
        self.lossPerElement = tf.nn.ctc_loss(labels=self.gtTexts, inputs=self.savedCtcInput,
                                             sequence_length=self.seqLen, ctc_merge_repeated=True)

        # decoder: either best path decoding or beam search decoding
        # TODO decodertypes weggehaald.
        self.decoder = tf.nn.ctc_greedy_decoder(inputs=self.ctcIn3dTBC, sequence_length=self.seqLen)

    def inferBatch(self, batch, calc_probability=False):
        """
        feed a batch into the NN to recognize the texts
        """

        # decode, optionally save RNN output
        numBatchElements = len(batch.image)
        evalList = [self.decoder] + [self.ctcIn3dTBC]
        feedDict = {self.input_image: batch.image, self.seqLen: [Model.max_text_length] * numBatchElements}
        evalRes = self.sess.run(evalList, feedDict)
        decoded = evalRes[0]
        texts = self.decoderOutputToText(decoded, numBatchElements)

        # feed RNN output and recognized text into CTC loss to compute labeling probability
        probs = None
        if calc_probability:
            sparse = self.toSparse(texts)
            ctcInput = evalRes[1]
            evalList = self.lossPerElement
            feedDict = {self.savedCtcInput: ctcInput, self.gtTexts: sparse,
                        self.seqLen: [Model.max_text_length] * numBatchElements}
            lossVals = self.sess.run(evalList, feedDict)
            probs = np.exp(-lossVals)

        return (texts, probs)

    def decoderOutputToText(self, ctcOutput, batchSize):
        """
        extract texts from output of CTC decoder
        """

        # contains string of labels for each batch element
        encodedLabelStrs = [[] for i in range(batchSize)]

        # TODO wat decodertypes weggehaald. nog wel kijken of andere decodertypes beter resultaat geven.
        # ctc returns tuple, first element is SparseTensor
        decoded = ctcOutput[0][0]

        # go over all indices and save mapping: batch -> values
        for (idx, idx2d) in enumerate(decoded.indices):
            label = decoded.values[idx]
            batchElement = idx2d[0]  # index according to [b,t]
            encodedLabelStrs[batchElement].append(label)

        # map labels to chars for all batch elements
        return [str().join([self.char_list[c] for c in labelStr]) for labelStr in encodedLabelStrs]

    def toSparse(self, texts=None):
        """
        put ground truth texts into sparse tensor for ctc_loss
        """
        indices = []
        values = []
        shape = [len(texts), 0]  # last entry must be max(labelList[i])

        # go over all texts
        for (batchElement, text) in enumerate(texts):
            # convert to string of label (i.e. class-ids)
            labelStr = [self.char_list.index(c) for c in text]
            # sparse tensor must have size of max. label-string
            if len(labelStr) > shape[1]:
                shape[1] = len(labelStr)
            # put each label into sparse tensor
            for (i, label) in enumerate(labelStr):
                indices.append([batchElement, i])
                values.append(label)

        return (indices, values, shape)

