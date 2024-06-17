package it.unipi.cloud.inmappingcombiner;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.Text;

//fai una hashmap con le lettere e il loro conteggio

public class LetterTotalCount {

    private final static LongWritable one = new LongWritable(1);
    private Text word = new Text("total");

    public static class CounterMapper extends Mapper<Object, Text, Text, LongWritable> 
    {

        Map<Text, LongWritable> letterCount;
        private Integer sumTotal = 0;

        public void setup(Context context) {
            letterCount = new HashMap<Text, LongWritable>();
        }

        @Override
        public void map(Object key, Text value, Mapper<Object, Text, Text, LongWritable>.Context context) throws IOException, InterruptedException {
        String line = value.toString();
        for (char c : line.toCharArray()) {
            if (Character.isLetter(c)) {
                    sumTotal++;
                }
            }
            letterCount.put(sumTotal, one);
        }

        public void cleanup(Context context) throws IOException, InterruptedException {
            for (Map.Entry<Text, LongWritable> entry : letterCount.entrySet()) {
                context.write(entry.getKey(), sumTotal); //might insert directly one here
            }
        }
    }

    public static class CounterReducer extends Reducer<Text, LongWritable, NullWritable, LongWritable> 
    {
        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Reducer<Text, LongWritable, NullWritable, LongWritable>.Context context) throws IOException, InterruptedException {
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            context.write(key, sum);
        }
    }   
}
