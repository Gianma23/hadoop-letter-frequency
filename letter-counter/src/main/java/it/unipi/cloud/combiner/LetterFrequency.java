package it.unipi.cloud.combiner;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.Text;

public class LetterFrequency {
    public static class CounterMapper extends Mapper<Object, Text, NullWritable, LongWritable> 
    {}

    public static class CounterReducer extends Reducer<NullWritable, LongWritable, NullWritable, LongWritable> 
    {}
}
