package it.unipi.cloud;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.GenericOptionsParser;
// TODO conditionally import the correct classes
import it.unipi.cloud.combiner.LetterTotalCount;
import it.unipi.cloud.combiner.LetterFrequency;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MapReduceApp {

    private static final int NUMBER_OF_REDUCERS = 3;
    private static final int INPUT_INDEX = 1;
    private static final int OUTPUT_LETTERCOUNT_INDEX = 2;
    private static final int OUTPUT_LETTERFREQ_INDEX = 3;

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

        Job countJob = Job.getInstance(conf, "Total Letter Count");
        countJob.setJarByClass(LetterTotalCount.class);
        countJob.setMapperClass(LetterTotalCount.CounterMapper.class);
        countJob.setCombinerClass(LetterTotalCount.CounterReducer.class);
        countJob.setReducerClass(LetterTotalCount.CounterReducer.class);
        
        countJob.setOutputKeyClass(org.apache.hadoop.io.Text.class);
        countJob.setOutputValueClass(org.apache.hadoop.io.LongWritable.class);

        FileInputFormat.addInputPath(countJob, new Path(otherArgs[INPUT_INDEX]));
        FileOutputFormat.setOutputPath(countJob, new Path(otherArgs[OUTPUT_LETTERCOUNT_INDEX]));

        if(!countJob.waitForCompletion(true)){
            System.exit(1);
        }

        long letterCount = getLetterCount(countJob);
        
        Job freqJob = Job.getInstance(conf, "Letter Frequency");
        freqJob.setJarByClass(LetterFrequency.class);
        freqJob.setMapperClass(LetterFrequency.CounterMapper.class);
        freqJob.setCombinerClass(LetterFrequency.CounterReducer.class);
        freqJob.setReducerClass(LetterFrequency.CounterReducer.class);

        freqJob.setNumReduceTasks(NUMBER_OF_REDUCERS);

        countJob.setOutputKeyClass(org.apache.hadoop.io.Text.class);
        countJob.setOutputValueClass(org.apache.hadoop.io.LongWritable.class);

        FileInputFormat.addInputPath(freqJob, new Path(otherArgs[INPUT_INDEX]));
        FileOutputFormat.setOutputPath(freqJob, new Path(otherArgs[OUTPUT_LETTERFREQ_INDEX]));

        System.exit(freqJob.waitForCompletion(true) ? 0 : 1);
    }

    private static long getLetterCount(Job job) {

        return 0;
    }
}