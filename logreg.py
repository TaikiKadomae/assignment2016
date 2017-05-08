import sys
import numpy as np
import tensorflow as tf

LOG_DIR = "/home/kadomae.13029/kadai/log/"
vocab_size = 0
def read_instance(s):
    index = []
    splitLine = s.strip().split(' ')
    i = 0
    for j in splitLine:
        if (j != splitLine[0]):
            feature = j.split(':')
            for i in range(int(feature[1])):
                index.append(int(feature[0]))

    tup = (splitLine[0],index)
    return tup

def read_data(train, feature_size):
    dataList = []
    
    for i in open(train).readlines():
        tup = read_instance(i)
        dataList.append(tup)

    for j in dataList:
        maxindex = max(j[1])
    
    
    if (feature_size >= 0):
        newdata = []
        for data in dataList:
            if (len(data[1]) > feature_size):
                newdata.append((data[0],data[1][:feature_size]))
            else:
                newdata.append((data[0], data[1]))

        return (newdata, maxindex + 1)
    
    else:    
        return (dataList, maxindex + 1)

def fill_feed_dict(data):
    label = []
    vectors = []
    for l, v in data:
        label.append(l)
        vectors.append(v)
    
    feed = {inputs:vectors,
            labels:label}
    return feed


def list_data(data, update_vocab=True):
    global vocab_size
    labels = []
    inputs = []
    for instance in data:
        label = [0.0, 1.0] if instance[0] == "1" else [1.0, 0.0]
        input_vec = np.int32(instance[1])
        labels.append(np.float32(label))
        mid = np.max(input_vec)
        if update_vocab is True:
            if mid+1 > vocab_size:
                vocab_size = mid+1
        else:
            if mid+1 > vocab_size:
                input_vec = np.int32([i if i < vocab_size else 0 for i in input_vec])
        inputs.append(input_vec)
        
    return labels, inputs


if __name__ == "__main__":
    feature_size = 5000
    emb_dim = 50
    epoch = 100
    train_data, train_vocab_size = read_data(sys.argv[1], feature_size)
    devel_data, devel_vocab_size = read_data(sys.argv[2], feature_size)
    graph = tf.Graph()
    with graph.as_default():
        with tf.name_scope(u'place_holder') as scope:
            inputs = tf.placeholder(tf.int32, shape=[None])
            labels = tf.placeholder(tf.float32, shape= [2])

        embeddings = tf.Variable(tf.random_uniform([train_vocab_size, emb_dim]))
        embeds = tf.nn.embedding_lookup(embeddings, inputs)

        with tf.name_scope(u'hidden_layer') as scope:
            h = tf.reduce_mean(embeds, reduction_indices=[0])
            w = tf.Variable(tf.random_uniform([emb_dim,2], -1.0, 1.0))
            b = tf.Variable(tf.random_uniform([2], -1.0, 1.0))
            h_dropout = tf.nn.dropout(h, 0.5)
            l2 = tf.nn.l2_loss(w)
            l2_lambda = 0.01
        with tf.name_scope(u'softmax') as scope:
            y = tf.nn.softmax(tf.matmul(tf.reshape(h, [-1, emb_dim]), w) + b)

        with tf.name_scope(u'loss') as scope:
            cross_entropy = tf.reduce_mean(-tf.reduce_sum(labels * tf.log(y)))
            loss = cross_entropy + l2_lambda*l2
            train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

        with tf.name_scope(u'test') as scope:
            acc_op, acc_update_op = tf.metrics.accuracy(tf.argmax(labels, 0), tf.argmax(tf.reshape(y,[2]), 0))
            
        loss_sum = tf.summary.scalar('loss',loss)
        acc_sum = tf.summary.scalar('accuracy', acc_update_op)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        g_init = tf.global_variables_initializer()
        l_init = tf.local_variables_initializer()
        sess.run(g_init)
        sess.run(l_init)
        summary_op = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter(LOG_DIR,graph_def=sess.graph_def)
        #feed_dict = fill_feed_dict(train_data)
        print('--------------train start--------------')
        labs, inps = list_data(train_data)
        assert(vocab_size == train_vocab_size)
        for ep in range(epoch):
            losses = []
            shuffled = list(zip(labs, inps))
            np.random.shuffle(shuffled)
            for iy, ix in shuffled:
                _, s, l, a = sess.run([train_step,summary_op, cross_entropy, acc_update_op], feed_dict={inputs: ix, labels: iy})
                summary_str = sess.run([])
            losses.append(l)
            summary_writer.add_summary(s,ep)
            print("epoch", ep, ":",sum(losses) / len(losses))
        print('------------evaluation start-----------')
        #correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(labels,1))
        #acc = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
        #acc_op, acc_update_op = tf.metrics.accuracy(tf.argmax(labels, 0), tf.argmax(tf.reshape(y, [2]), 0))
        labs_d, inps_d = list_data(devel_data, update_vocab=False)
        #sess.run(tf.local_variables_initializer())
        for iy, ix in zip(labs_d, inps_d):
            sess.run(acc_update_op, feed_dict={inputs:ix, labels:iy})
        acc = sess.run(acc_op)
        #print(sess.run(acc, feed_dict={inputs: inps_d, labels: labs_d}))
        print(acc)
