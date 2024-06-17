package it.unipi.cloud.combiner;

import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.Text;

public class LetterFrequency {
    public static class CounterMapper extends Mapper<LongWritable, Text, Text, LongWritable> 
    {
        private LongWritable one = new LongWritable(1);

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
        {
            Text letter = new Text();
            String line = value.toString();
            for (char c : line.toCharArray()) {
                if (Character.isLetter(c)) {
                    letter.set(Character.toString(Character.toLowerCase(c)));
                    context.write(letter, one);
                }
            }
        }
    }

    public static class CounterCombiner extends Reducer<Text, LongWritable, Text, LongWritable> 
    {
        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException
        {
            LongWritable result = new LongWritable();
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static class CounterReducer extends Reducer<Text, LongWritable, Text, DoubleWritable> 
    {
        private long letterCount;

        public void setup(Context context) {
            letterCount = context.getConfiguration().getLong("letterCount", 1);
        }

        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException
        {
            DoubleWritable result = new DoubleWritable();
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            
            double freq = (double) sum / (double) letterCount;
            result.set(freq);
            context.write(key, result);
        }
    }
}