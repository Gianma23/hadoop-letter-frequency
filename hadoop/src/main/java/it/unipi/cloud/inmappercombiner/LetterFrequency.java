package it.unipi.cloud.inmappercombiner;

import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import it.unipi.cloud.utils.StringUtils;
import org.apache.hadoop.io.Text;
import java.util.HashMap;

public class LetterFrequency {

    public static class CounterMapper extends Mapper<LongWritable, Text, Text, LongWritable> {
        private LongWritable one = new LongWritable(1);
        HashMap<Text, LongWritable> letterCount;

        @Override
        public void setup(Context context) {
            letterCount = new HashMap<Text, LongWritable>();
        }

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = StringUtils.normalizeString(value.toString());
            for (char c : line.toCharArray()) {
                Text letter = new Text();
                LongWritable newValue = new LongWritable();
            
                String letterStr = Character.toString(Character.toLowerCase(c));
                if (!StringUtils.isLetter(letterStr)) {
                    continue;
                }
                letter.set(letterStr);
                if (letterCount.containsKey(letter)) {
                    newValue.set(letterCount.get(letter).get() + 1);
                    letterCount.put(letter, newValue);
                } else {
                    letterCount.put(letter, one);
                }
            }
        }

        @Override
        public void cleanup(Context context) throws IOException, InterruptedException {
            for (HashMap.Entry<Text, LongWritable> entry : letterCount.entrySet()) {
                context.write(entry.getKey(), entry.getValue());
            }
        }
    }

    public static class CounterReducer extends Reducer<Text, LongWritable, Text, DoubleWritable> {
        private long letterCount;

        @Override
        public void setup(Context context) {
            letterCount = context.getConfiguration().getLong("letterCount", 1);
        }

        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
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

