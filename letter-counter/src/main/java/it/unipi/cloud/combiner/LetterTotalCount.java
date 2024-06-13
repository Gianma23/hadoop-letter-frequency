package it.unipi.cloud.combiner;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.Text;

public class LetterTotalCount {

    private final static IntWritable one = new IntWritable(1);
    private final static Text word = new Text("total");


    public static class CounterMapper extends Mapper<Object, Text, Text, IntWritable> 
    {
        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] words = line.split("\\s+");
            for (String str : words) {
                if (!str.isEmpty()) {
                    context.write(word, one);
                }
            }
        }
    }

    public static class CounterReducer extends Reducer<Text, LongWritable, Text, LongWritable> 
    {
        private LongWritable result = new LongWritable();
        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }   
}
