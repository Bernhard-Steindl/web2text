package ch.ethz.dalab.web2text

import ch.ethz.dalab.web2text.utilities.Util
import ch.ethz.dalab.web2text.cleaneval.CleanEval
import ch.ethz.dalab.web2text.output.CsvDatasetWriter
import ch.ethz.dalab.web2text.features.{FeatureExtractor, PageFeatures}
import ch.ethz.dalab.web2text.features.extractor._


object Tmp {
  def main(args: Array[String]): Unit = {

    val unaryExtractor =
      DuplicateCountsExtractor + LeafBlockExtractor + AncestorExtractor(NodeBlockExtractor + TagExtractor(mode = "node"), 1) +
        AncestorExtractor(NodeBlockExtractor, 2) + RootExtractor(NodeBlockExtractor) + TagExtractor(mode = "leaf")

    val pairwiseExtractor =
      TreeDistanceExtractor +
        BlockBreakExtractor +
        CommonAncestorExtractor(NodeBlockExtractor)
    val fe = FeatureExtractor(unaryExtractor, pairwiseExtractor)
    // Write block_features.csv and edge_features.csv
    // Format of a row: page id, groundtruth label (1/0), features ...
    val data = Util.time {
      CleanEval.dataset(fe)
    }
    CsvDatasetWriter.write(data, "./src/main/python/data")
    // Print the names of the exported features in order
    println("# Block features")
    fe.blockExtractor.labels.foreach(println)
    println("# Edge features")
    fe.edgeExtractor.labels.foreach(println)

  }
}