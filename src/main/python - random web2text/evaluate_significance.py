import pandas as pd
import os

import numpy as np
from data import cleaneval

def gen_train_test_val_split(train_size=0.7, val_size=0.1, use_their_split_size=False):
  all_ids =  np.array([164, 648, 168, 505, 495, 563, 288, 321, 295, 242, 702, 332, 585, 712, 139, 520, 686, 204,
   545, 181, 344, 147, 359, 513, 498, 101, 339, 499, 329, 0, 493, 726, 518, 549, 11, 386
                 , 294, 6, 372, 18, 328, 369, 727, 13, 292, 556, 244, 488, 76, 403, 379, 206, 407, 610, 188, 112, 193,
              516, 133, 614, 30, 546, 317, 85, 544, 115, 657, 607, 231, 331, 4, 555, 274, 194, 310, 515
                 , 230, 60, 9, 56, 414, 404, 300, 156, 365, 606, 96, 646, 281, 304, 426, 149, 258, 734
                 , 305, 461, 569, 324, 185, 90, 670, 417, 604, 14, 270, 125, 655, 651, 422, 640, 677, 446
                 , 467, 236, 123, 457, 736, 487, 207, 592, 178, 287, 285, 444, 28, 165, 144, 347, 27, 580
                 , 384, 121, 94, 558, 708, 167, 526, 593, 678, 476, 95, 639, 552, 38, 725, 716, 514, 19
                 , 445, 169, 480, 301, 289, 129, 58, 150, 695, 35, 653, 201, 259, 373, 191, 349, 162, 376
                 , 591, 605, 306, 595, 584, 692, 25, 172, 117, 67, 401, 355, 221, 541, 637, 397, 430, 160
                 , 336, 572, 603, 690, 641, 88, 613, 492, 709, 509, 405, 225, 416, 632, 176, 685, 375, 48
                 , 277, 65, 562, 577, 154, 523, 33, 589, 391, 81, 319, 105, 297, 394, 667, 665, 507, 357
                 , 650, 453, 353, 691, 400, 214, 174, 31, 47, 330, 224, 533, 620, 276, 280, 590, 312, 198
                 , 696, 631, 92, 460, 521, 290, 618, 389, 537, 623, 146, 699, 364, 229, 418, 465, 170, 86
                 , 283, 113, 642, 666, 84, 663, 424, 578, 107, 587, 197, 661, 536, 73, 659, 468, 687, 219
                 , 609, 704, 44, 466, 89, 436, 551, 486, 322, 335, 218, 241, 116, 57, 21, 23, 581, 226
                 , 635, 212, 159, 710, 217, 647, 24, 228, 134, 361, 733, 388, 70, 1, 599, 722, 97, 724
                 , 720, 684, 502, 396, 703, 313, 385, 82, 272, 634, 175, 196, 77, 393, 398, 539, 611, 630
                 , 17, 621, 413, 104, 261, 586, 12, 69, 80, 220, 454, 689, 588, 654, 232, 250, 652, 315
                 , 491, 343, 617, 524, 7, 497, 719, 735, 98, 103, 293, 327, 540, 378, 688, 531, 489, 141
                 , 265, 132, 624, 660, 481, 255, 438, 671, 216, 561, 61, 464, 43, 51, 574, 383, 325, 463
                 , 439, 271, 99, 567, 597, 644, 700, 302, 535, 490, 143, 390, 40, 431, 456, 559, 530, 66
                 , 120, 279, 434, 326, 411, 74, 55, 423, 449, 504, 32, 568, 227, 184, 462, 138, 153, 209
                 , 253, 233, 571, 245, 203, 223, 257, 420, 583, 36, 676, 39, 474, 263, 717, 433, 625, 706
                 , 707, 148, 273, 399, 22, 10, 49, 512, 366, 249, 675, 478, 199, 79, 356, 517, 237, 669
                 , 511, 71, 395, 519, 41, 189, 42, 715, 46, 342, 662, 308, 668, 547, 358, 351, 412, 485
                 , 713, 128, 296, 529, 626, 151, 182, 508, 251, 527, 155, 565, 543, 455, 573, 348, 638, 560
                 , 282, 442, 674, 68, 211, 109, 601, 557, 368, 510, 387, 370, 409, 186, 337, 419, 268, 622
                 , 408, 114, 382, 550, 137, 363, 350, 135, 679, 619, 582, 34, 340, 286, 723, 163, 380, 470
                 , 111, 410, 360, 528, 256, 482, 53, 731, 553, 180, 264, 338, 477, 664, 119, 501, 672, 72
                 , 425, 341, 564, 496, 440, 262, 131, 307, 374, 269, 248, 681, 377, 729, 698, 190, 579, 447
                 , 475, 354, 680, 402, 532, 200, 575, 267, 318, 548, 3, 161, 320, 415, 479, 171, 371, 16
                 , 316, 483, 645, 298, 179, 75, 730, 124, 78, 309, 87, 534, 705, 362, 192, 247, 538, 311, 29, 494, 202, 210, 636, 183, 238, 628, 64
                 , 126, 469, 345, 429, 732, 697, 235, 566, 234, 108, 62, 158, 484, 299, 503, 459, 643, 213
                 , 243, 522, 656, 506, 291, 50, 110, 714, 406, 711, 303, 435, 633, 260, 701, 142, 421, 240
                 , 59, 187, 314, 2, 136, 682, 54, 602, 427, 718, 157, 381, 195, 127, 683, 392, 5, 122
                 , 93, 451, 629, 83, 616, 458, 542, 334, 428, 596, 205, 693, 91, 177, 215, 252, 140, 500
                 , 649, 448, 443, 594, 728, 266, 239, 554, 570, 452, 152, 323, 576, 598, 473, 100, 173, 275
                 , 627, 525, 8, 284, 26, 37, 130, 472, 208, 222, 352, 52, 45, 367, 278, 106, 615, 15
                 , 432, 246, 166, 721, 145, 63, 608, 694, 346, 600, 450, 612, 441, 102, 20, 658, 471, 673
                 , 118, 333, 437, 254
              ])
  np.random.shuffle(all_ids)
  train_size = int(len(all_ids)*train_size)
  val_size = int(len(all_ids)*val_size)
  if use_their_split_size:
    # use the split sizes of their paper
    train_size=531
    val_size=58
  train_ids = all_ids[:train_size]
  val_ids = all_ids[train_size:train_size+val_size]
  test_ids = all_ids[train_size+val_size:]
  np.save("train_ids.npy", train_ids)
  np.save("val_ids.npy", val_ids)
  np.save("test_ids.npy", test_ids)

def run_random_split():
  for i in range(20):
    gen_train_test_val_split(use_their_split_size=True)
    os.system("python3 main.py train_unary custom")
    os.system("python3 main.py train_edge custom")
    os.system("python3 main.py test_structured custom")




if __name__ == "__main__":
  run_random_split()
  raise Exception("Done")

  for i in range(20):
    os.system("python3 main.py train_unary")
    os.system("python3 main.py train_edge")
    os.system("python3 main.py test_structured")

  columns=["_","accuracy", "precision", "recall", "f1", "accuracy_u", "precision_u", "recall_u", "f1_u"]
  df = pd.read_csv("cleaneval.csv")

  df.columns = columns

  print(df)