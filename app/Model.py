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
        cnn_out4d = self.setup_cnn()
        rnn_out3d = self.setup_rnn(cnn_out4d)
        self.setup_ctc(rnn_out3d)

        # initialize TF
        (self.sess, self.saver) = setup_tf()

    def setup_cnn(self):
        """
        create CNN layers and return output of these layers
        """
        cnn_in4d = tf.expand_dims(input=self.input_image, axis=3)

        # list of parameters for the layers
        # TODO zijn dit de paramaters die we gaan gebruiken?
        kernel_vals = [5, 5, 3, 3, 3]
        feature_vals = [1, 32, 64, 128, 128, 256]
        stride_vals = poolVals = [(2, 2), (2, 2), (1, 2), (1, 2), (1, 2)]
        num_layers = len(stride_vals)

        # create layers
        pool = cnn_in4d  # input to first CNN layer
        for i in range(num_layers):
            kernel = tf.Variable(
                tf.truncated_normal([kernel_vals[i], kernel_vals[i], feature_vals[i], feature_vals[i + 1]], stddev=0.1))
            conv = tf.nn.conv2d(pool, kernel, padding='SAME', strides=(1, 1, 1, 1))
            conv_norm = tf.layers.batch_normalization(conv)
            relu = tf.nn.relu(conv_norm)
            pool = tf.nn.max_pool(relu, (1, poolVals[i][0], poolVals[i][1], 1),
                                  (1, stride_vals[i][0], stride_vals[i][1], 1), 'VALID')

        return pool

    def setup_rnn(self, cnn_out4d):
        """
        create RNN layers and return output of these layers
        """
        rnn_in3d = tf.squeeze(cnn_out4d, axis=[2])

        # basic cells which is used to build RNN
        num_hidden = 256
        cells = [tf.contrib.rnn.LSTMCell(num_units=num_hidden, state_is_tuple=True) for _ in range(2)]  # 2 layers

        # stack basic cells
        stacked = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        # bidirectional RNN
        # BxTxF -> BxTx2H
        ((fw, bw), _) = tf.nn.bidirectional_dynamic_rnn(cell_fw=stacked, cell_bw=stacked, inputs=rnn_in3d,
                                                        dtype=rnn_in3d.dtype)

        # BxTxH + BxTxH -> BxTx2H -> BxTx1X2H
        concat = tf.expand_dims(tf.concat([fw, bw], 2), 2)

        # project output to chars (including blank): BxTx1x2H -> BxTx1xC -> BxTxC
        kernel = tf.Variable(tf.truncated_normal([1, 1, num_hidden * 2, len(self.char_list) + 1], stddev=0.1))
        return tf.squeeze(tf.nn.atrous_conv2d(value=concat, filters=kernel, rate=1, padding='SAME'), axis=[2])

    def setup_ctc(self, rnn_out3d):
        """
        create CTC loss and decoder and return them
        """
        # BxTxC -> TxBxC
        self.ctc_in3d_tbc = tf.transpose(rnn_out3d, [1, 0, 2])
        # ground truth text as sparse tensor
        self.get_texts = tf.SparseTensor(tf.placeholder(tf.int64, shape=[None, 2]), tf.placeholder(tf.int32, [None]),
                                         tf.placeholder(tf.int64, [2]))

        # calc loss for batch
        self.seq_len = tf.placeholder(tf.int32, [None])
        self.loss = tf.reduce_mean(
            tf.nn.ctc_loss(labels=self.get_texts, inputs=self.ctc_in3d_tbc, sequence_length=self.seq_len,
                           ctc_merge_repeated=True))

        # calc loss for each element to compute label probability
        self.saved_ctc_input = tf.placeholder(tf.float32, shape=[Model.max_text_length, None, len(self.char_list) + 1])
        self.loss_per_element = tf.nn.ctc_loss(labels=self.get_texts, inputs=self.saved_ctc_input,
                                               sequence_length=self.seq_len, ctc_merge_repeated=True)

        # decoder: either best path decoding or beam search decoding
        # TODO decodertypes weggehaald.
        self.decoder = tf.nn.ctc_greedy_decoder(inputs=self.ctc_in3d_tbc, sequence_length=self.seq_len)

    def infer_batch(self, batch, calc_probability=False):
        """
        feed a batch into the NN to recognize the texts
        """

        # decode, optionally save RNN output
        num_batch_elements = len(batch.image)
        eval_list = [self.decoder] + [self.ctc_in3d_tbc]
        feed_dict = {self.input_image: batch.image, self.seq_len: [Model.max_text_length] * num_batch_elements}
        eval_res = self.sess.run(eval_list, feed_dict)
        decoded = eval_res[0]
        texts = self.decoder_output_to_text(decoded, num_batch_elements)

        # feed RNN output and recognized text into CTC loss to compute labeling probability
        probability = None
        if calc_probability:
            sparse = self.to_sparse(texts)
            ctc_input = eval_res[1]
            eval_list = self.loss_per_element
            feed_dict = {self.saved_ctc_input: ctc_input, self.get_texts: sparse,
                         self.seq_len: [Model.max_text_length] * num_batch_elements}
            loss_values = self.sess.run(eval_list, feed_dict)
            probability = np.exp(-loss_values)

        return texts, probability

    def decoder_output_to_text(self, ctcOutput, batchSize):
        """
        extract texts from output of CTC decoder
        """

        # contains string of labels for each batch element
        encoded_label_strs = [[] for i in range(batchSize)]

        # TODO wat decodertypes weggehaald. nog wel kijken of andere decodertypes beter resultaat geven.
        # ctc returns tuple, first element is SparseTensor
        decoded = ctcOutput[0][0]

        # go over all indices and save mapping: batch -> values
        for (idx, idx2d) in enumerate(decoded.indices):
            label = decoded.values[idx]
            batch_element = idx2d[0]  # index according to [b,t]
            encoded_label_strs[batch_element].append(label)

        # map labels to chars for all batch elements
        return [str().join([self.char_list[c] for c in labelStr]) for labelStr in encoded_label_strs]

    def to_sparse(self, texts=None):
        """
        put ground truth texts into sparse tensor for ctc_loss
        """
        indices = []
        values = []
        shape = [len(texts), 0]  # last entry must be max(labelList[i])

        # go over all texts
        for (batch_element, text) in enumerate(texts):
            # convert to string of label (i.e. class-ids)
            label_string = [self.char_list.index(c) for c in text]
            # sparse tensor must have size of max. label-string
            if len(label_string) > shape[1]:
                shape[1] = len(label_string)
            # put each label into sparse tensor
            for (i, label) in enumerate(label_string):
                indices.append([batch_element, i])
                values.append(label)

        return indices, values, shape
