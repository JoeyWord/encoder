# coding=utf-8

import time
import os
import pdb
import tensorflow as tf
import sys
sys.path.append('/mnt/nlp')
#pdb.set_trace()
from data_utils import get_log,make_path,load_config,save_config,print_config,all_config,sentence2id,id2sentence
from seq2seq.data_pre import dataManager
from seq2seq.annotationSeq2Seq import Seq2SeqModel
from seq2seq.batch_dataset import Seq2SeqDataset
from seq2seq.encoder_sentence import EncoderSentence
from seq2seq.pttModel import PTTModel,run_epoch,make_list,makeBatches

#chdir
cur_dir = os.getcwd()
if os.path.basename(cur_dir) != "seq2seq":
    os.chdir("/mnt/nlp/seq2seq")

FLAGS = tf.app.flags
FLAGS.DEFINE_integer('hidden_size', 1024, 'size of hidden units')
FLAGS.DEFINE_integer('num_layers', 2, 'number of layers')
FLAGS.DEFINE_integer('batch_size', 100, 'size of batch')
FLAGS.DEFINE_integer('time_step', 20, 'sequence length')
FLAGS.DEFINE_integer('image_size', 299, 'size of image')
FLAGS.DEFINE_integer('channel', 3, 'channel num of image')
FLAGS.DEFINE_integer('epoch', 5, 'epoch nums for training')
FLAGS.DEFINE_integer('max_to_keep', 3, 'max num step for saving model')
FLAGS.DEFINE_integer('max_dec_len', 100, 'max length of decoding sentence')
FLAGS.DEFINE_integer('src_vocab_size', 10000, 'words num of src file')
FLAGS.DEFINE_integer('trg_vocab_size', 4000, 'words num of trg file')
FLAGS.DEFINE_integer('vocab_size',10000,'words num of ptt file')
FLAGS.DEFINE_integer('decay_step', 50, 'decay coef compute steps')
FLAGS.DEFINE_integer('sos_id', 0, 'id of sos')
FLAGS.DEFINE_integer('eos_id', 1, 'id of eos')
FLAGS.DEFINE_integer('clip_norm', 5, 'adjust the gradent to preventing ecolipse')
FLAGS.DEFINE_integer('n_class', 10, 'specify the class of classify problem')
FLAGS.DEFINE_integer('shuffle_size', 1000, 'dataset shuffle size')
FLAGS.DEFINE_integer('max_size', 50, 'max sentence size to limit')

FLAGS.DEFINE_float('learning_rate', 0.01, 'optimializer for learning rate')
FLAGS.DEFINE_float('decay_rate', 0.05, 'decay rate compute')
FLAGS.DEFINE_float('keep_prob', 0.9, 'drop out prob for rnn multi_layers')
FLAGS.DEFINE_float('input_keep_prob', 0.8, 'drop out prob for embedding layer')


FLAGS.DEFINE_string('config_file', os.path.join('config','all_info.cfg'), 'store info of config')
FLAGS.DEFINE_string('log_file', os.path.join('log','seq2seq.log'), 'file to store log')
FLAGS.DEFINE_string('vocab_file', 'vocab.txt', 'file with vocab info')
FLAGS.DEFINE_string('src_ids', os.path.join('data','en-zh/en-zh_ids.en'), 'src file train input with ids ')
FLAGS.DEFINE_string('trg_ids', os.path.join('data','en-zh/en-zh_ids.zh'), 'target file train input with ids')
FLAGS.DEFINE_string('src_input', os.path.join('data', 'en-zh/en-zh.en.token'), 'en spilt info as src file')
FLAGS.DEFINE_string('trg_input', os.path.join('data', 'en-zh/en-zh.zh.token'), 'zh split info as trg file')
FLAGS.DEFINE_string('ckpt_path', 'ckpt', 'path to store model')
FLAGS.DEFINE_string('project_path', "/mnt/nlp/seq2seq", 'root path of project')
FLAGS.DEFINE_string('vocab_src', 'vocab_src.txt', 'store the word info of english')
FLAGS.DEFINE_string('vocab_trg', 'vocab_trg.txt', 'store the word info of chinese')

FLAGS.DEFINE_boolean('seq2seq',False,'specify run which model')
FLAGS.DEFINE_boolean('share_embedding_params',True,'share embedding params or not')
FLAGS.DEFINE_boolean('is_decay', True, 'learning rate belong decay train format')
FLAGS.DEFINE_boolean('add_attention', False, 'specify seq2seq model use annotation')

FLAGS = tf.app.flags.FLAGS
#target word info transfer into id info


def main(_):
    make_path(FLAGS.project_path,"seq2seq")
    if not os.path.isfile(FLAGS.config_file):
        config = all_config(FLAGS)
        save_config(config,FLAGS.config_file)
    else:
        config = load_config(FLAGS.config_file)
    if FLAGS.seq2seq:
        logger = get_log(FLAGS.log_file)
        print_config(config,logger)
        src_word2id, src_id2word = dataManager.word_statics(FLAGS.src_input,FLAGS.vocab_src,config["svs"])

        trg_word2id, trg_id2word = dataManager.word_statics(FLAGS.trg_input,FLAGS.vocab_trg,config["tvs"])

        # test sentence fot translating
        #check ckpt model file
        logger.info("begain test sentence input...")
        sentence = "<sos>this is a test<eos>"
        sentence_input = sentence2id(sentence,src_word2id)
        encoderSentence = EncoderSentence(config,logger)
        target_ids = encoderSentence.inference(sentence_input)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(FLAGS.ckpt_path)
            if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_file):
                saver.restore(sess,ckpt.model_checkpoint_file)
                translate_out = sess.run(target_ids)
            else:
            	# load dataset
				time0 = time.time()
				logger.info("begain load dataset from PTB...")
		        datasetSeq2Seq = Seq2SeqDataset(config)
		        src_trgDataset = datasetSeq2Seq.padding_dataset

		        iterator = src_trgDataset.make_initializable_iterator()
		        (src, src_size), (trg_input, trg_label, trg_size) = iterator.get_next()
		        time1 = time.time()
		        logger.info("load dataset successful and cost time:{}".format(time1-time0))
		        seq2seq_model = Seq2SeqModel(config, logger)
		        loss, train_op = seq2seq_model.seq2seqModel(src, src_size, trg_input, trg_label, trg_size)
		        step = 0
		        
	            sess.run(tf.global_variables_initializer())
	            logger.info("begain train model...")
	            time2 = time.time()
	            for epoch in range(FLAGS.epoch):
	                sess.run(iterator.initializer)
	                #pdb.set_trace()
	                step = seq2seq_model.run_epoch(sess,loss,train_op,FLAGS.ckpt_path,step)
	            time3 = time.time()
	            logger.info("model train over cost time:%9.5f(min)" %((time3-time2)/60))

        translate_res = id2sentence(translate_out,trg_id2word)
        logger.info("the translate result is: ".format(translate_res))
    else:
        logger = get_log('log/ptt_model.log')
        print_config(config,logger)
        logger.info("begain generate ids file...")
        train_ids = make_list(os.path.join(FLAGS.project_path,'data/train_id.txt'))
        valid_ids = make_list(os.path.join(FLAGS.project_path,'data/valid_id.txt'))
        test_ids = make_list(os.path.join(FLAGS.project_path,'data/test_id.txt'))
        logger.info("begain generate batches data for model...")
        train_batches = makeBatches(train_ids,config,is_train=True)
        valid_batch = makeBatches(valid_ids,config,is_train=False)
        test_batch = makeBatches(test_ids,config,is_train=False)
        #pdb.set_trace()
        logger.info("begain train model and test...")
        with tf.variable_scope("ptt_model", reuse=None):
            train_model = PTTModel(config, logger, True)
        #share params with train model
        with tf.variable_scope("ptt_model", reuse=True):
            eval_model = PTTModel(config, logger, False)
        step = 0
        time0 = time.time()
        with tf.Session() as sess:
            sess.run((tf.global_variables_initializer(),tf.local_variables_initializer()))
            for epoch in range(FLAGS.epoch):
                logger.info("iteration %d start:" %(epoch+1))
                ppl,step = run_epoch(sess, train_model, train_batches, num_step=step)
                ppl,_ = run_epoch(sess, eval_model, valid_batch, num_step=0)
                logger.info("after iteration %d model perplexity %.3f" %(epoch+1,ppl))
            time1 = time.time()
            logger.info("training ptt model cost time %5.2f(min)" %(time1-time0)/60)
            ppl,_ = run_epoch(sess, eval_model, test_batch, num_step=step)
            logger.info("after iteration %d test data perplexity %.3f" %(FLAGS.epoch,ppl))

if __name__ == '__main__':
    tf.app.run()
