import os


import numpy as np
from main import evaluate_unary
import tensorflow as tf
from forward import EDGE_VARIABLES, UNARY_VARIABLES, edge, loss, unary
from data import  our_new_test
from viterbi import viterbi

BATCH_SIZE = 128
PATCH_SIZE = 9
N_FEATURES = 128
N_EDGE_FEATURES = 25
TRAIN_STEPS = 5000
LEARNING_RATE = 1e-3
DROPOUT_KEEP_PROB = 0.8
REGULARIZATION_STRENGTH = 0.000
EDGE_LAMBDA = 1
CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), 'reproduce_model_our_new_split')




def evaluate(lamb=EDGE_LAMBDA):
  from data import cleaneval_test, cleaneval_train, cleaneval_validation

  test = our_new_test

  unary_features = tf.placeholder(tf.float32)
  edge_features  = tf.placeholder(tf.float32)

  # hack to get the right shape weights
  _ = unary(tf.placeholder(tf.float32, shape=[1,PATCH_SIZE,1,N_FEATURES]), False)
  _ = edge(tf.placeholder(tf.float32, shape=[1,PATCH_SIZE,1,N_EDGE_FEATURES]), False)

  tf.get_variable_scope().reuse_variables()
  unary_logits = unary(unary_features, is_training=False)
  edge_logits  = edge(edge_features, is_training=False)

  unary_saver = tf.train.Saver(tf.get_collection(UNARY_VARIABLES))
  edge_saver  = tf.train.Saver(tf.get_collection(EDGE_VARIABLES))

  init_op = tf.global_variables_initializer()

  with tf.Session() as session:
    session.run(init_op)
    unary_saver.restore(session, os.path.join(CHECKPOINT_DIR, "unary.ckpt"))
    edge_saver.restore(session, os.path.join(CHECKPOINT_DIR, "edge.ckpt"))

    from time import time

    start = time()
    def prediction_structured(features, edge_feat):
      features  = features[np.newaxis, :, np.newaxis, :]
      edge_feat = edge_feat[np.newaxis, :, np.newaxis, :]

      unary_lgts = session.run(unary_logits, feed_dict={unary_features: features})
      edge_lgts = session.run(edge_logits, feed_dict={edge_features: edge_feat})

      return viterbi(unary_lgts.reshape([-1,2]), edge_lgts.reshape([-1,4]), lam=lamb)

    def prediction_unary(features, _):
      features = features[np.newaxis, :, np.newaxis, :]
      logits = session.run(unary_logits, feed_dict={unary_features: features})
      return np.argmax(logits, axis=-1).flatten()

    accuracy, precision, recall, f1 = evaluate_unary(test, prediction_structured)
    accuracy_u, precision_u, recall_u, f1_u = evaluate_unary(test, prediction_unary)
    end = time()
    print('duration', end-start)
    print('size', len(test))
    print("Structured: Accuracy=%.5f, precision=%.5f, recall=%.5f, F1=%.5f" % (accuracy, precision, recall, f1))
    print("Just unary: Accuracy=%.5f, precision=%.5f, recall=%.5f, F1=%.5f" % (accuracy_u, precision_u, recall_u, f1_u))



if __name__ == "__main__":
    evaluate()