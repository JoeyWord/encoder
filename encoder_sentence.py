# coding=utf-8
import tensorflow as tf

from seq2seq.annotationSeq2Seq import Seq2SeqModel
class EncoderSentence(Seq2SeqModel):
    def __init__(self,config,logger):
        Seq2SeqModel.__init__(self,config,logger)
        self.max_dec_len = config['mdl']
        self.sos_id = config["sid"]
        self.eos_id = config["eid"]

    def inference(self,src):
        """
        encode the input sentence by while_loop
        :param src: list--input sentence ids
        :return: list--trg_ids(decode result)
        """
        #convert input src as one batch to feed into dynamic_rnn
        src_input = tf.convert_to_tensor([src],dtype=tf.int32,name='src_input')
        src_size = tf.convert_to_tensor([len(src)],dtype=tf.int32,name="src_size")
        src_emb = tf.nn.embedding_lookup(self.src_embedding,src_input)
        with tf.variable_scope("encoder",reuse=True):
            enc_out,enc_state = tf.nn.dynamic_rnn(self.enc_cell,src_emb,sequence_length=src_size)

        #use while_loop to call_back id to be decoded
        with tf.variable_scope("seq2seqModel/sentence/translate"):
            init_array = tf.TensorArray(dtype=tf.int32,size=0,dynamic_size=True,clear_after_read=False)
            # write sos_id into array
            init_array.write(0,self.sos_id)
            init_var = (enc_state,init_array,0)

            #condition break:if id == <eos>.id | id >= max_dec_len
            def loop_cond(state,trg_ids,step):
                trg_id = trg_ids.read(step)
                cond = tf.logical_and(tf.equal(trg_id,self.eos_id),tf.less_equal(trg_id,self.max_dec_len))
                return tf.reduce_all(cond)

            def loop_process(state,trg_ids,step):
                trg_input = [trg_ids.read(step)]
                trg_emb = tf.nn.embedding_lookup(self.trg_embedding,trg_input)
                dec_out,dec_state = self.dec_cell.call(trg_emb,state)
                reshape_out = tf.reshape(dec_out,shape=[-1,self.hidden_size],name='reshape_out')
                logits = tf.matmul(reshape_out,self.weight_out) + self.bias_out
                next_id = tf.argmax(logits,axis=-1,name="next_id")
                trg_ids.write((step+1),next_id[0])
                return state,trg_ids,step
            with tf.variable_scope("while_loop"):
                state,trg_ids,step = tf.while_loop(cond=loop_cond,body=loop_process,loop_vars=init_var)
            return trg_ids.stack()



