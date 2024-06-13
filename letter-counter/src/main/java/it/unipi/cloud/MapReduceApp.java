package it.unipi.cloud;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.GenericOptionsParser;

import it.unipi.cloud.combiner.LetterTotalCount;

import org.apache.hadoop.mapreduce.Job;

public class MapReduceApp {

    private static final int NUMBER_OF_REDUCERS = 1;

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

        Job countJob = Job.getInstance(conf, "Letter Counter");
        countJob.setJarByClass(LetterTotalCount.class);
        countJob.setMapperClass(it.unipi.cloud.combiner.LetterTotalCount.CounterMapper.class);
        countJob.setCombinerClass(it.unipi.cloud.combiner.LetterTotalCount.CounterReducer.class);
        countJob.setReducerClass(it.unipi.cloud.combiner.LetterTotalCount.CounterReducer.class);
        
        countJob.setNumReduceTasks(NUMBER_OF_REDUCERS);
    }
}