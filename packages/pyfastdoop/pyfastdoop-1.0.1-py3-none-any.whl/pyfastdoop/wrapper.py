from pyspark import SparkConf, SparkContext

class pyFastdoop:
    def __init__(self, sc=None):
        """ Initialize the wrapper with an existing SparkContext or create a new one """
        if sc is None:
            # Create a new SparkContext with the provided JAR path
            self.conf = SparkConf().setAppName("Fastdoop")
            self.sc = SparkContext(conf=self.conf)
        else:
            self.sc = sc  # Use the existing SparkContext

    def read_fasta(self, input_path, type="short"):
        """ Read FASTA files using Fastdoop's Hadoop InputFormat """
        if type == "short":
            rdd = self.sc.newAPIHadoopFile(
                input_path,
                inputFormatClass="fastdoop.FASTAshortInputFileFormat",
                keyClass="org.apache.hadoop.io.Text",
                valueClass="fastdoop.Record"
            )
        elif type == "long":
            rdd = self.sc.newAPIHadoopFile(
                input_path,
                inputFormatClass="fastdoop.FASTAlongInputFileFormat",
                keyClass="org.apache.hadoop.io.Text",
                valueClass="fastdoop.PartialSequence"
            )
        elif type == "fastq":
            rdd = self.sc.newAPIHadoopFile(
                input_path,
                inputFormatClass="fastdoop.FASTQInputFileFormat",
                keyClass="org.apache.hadoop.io.Text",
                valueClass="fastdoop.QRecord"
            )
        else:
            raise ValueError("Type must be either 'short', 'long' or 'fastq'")

        return rdd

    def print(self, rdd):
        """ Print contents of an RDD """
        for key, value in rdd.collect():
            print(f"Key: {key}, Value: {value}")

    def stop(self):
        """ Stop Spark Context """
        self.sc.stop()

# Example Usage with an Existing SparkContext
if __name__ == "__main__":
    # Assume SparkContext 'sc' is already initialized
    # If not, you can initialize it as below:
    sc = SparkContext(appName="ExistingContextApp")

    fastdoop = pyFastdoop(sc=sc)
    fasta_rdd = fastdoop.read_fasta("short.fasta", type="short")
    fastdoop.print(fasta_rdd)
    fastdoop.stop()