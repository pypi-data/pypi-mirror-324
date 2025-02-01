from pyspark import SparkConf, SparkContext
from pyfastdoop import pyFastdoop

if __name__ == "__main__":
    # Assume SparkContext 'sc' is already initialized
    # If not, you can initialize it as below:
    sc = SparkContext(appName="ExistingContextApp")

    fastdoop = pyFastdoop(sc=sc)
    fasta_rdd = fastdoop.read_fasta("short.fasta", type="short")
    fastdoop.print(fasta_rdd)
    fastdoop.stop()