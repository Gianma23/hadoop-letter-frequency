package it.unipi.cloud.combiner;

import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import it.unipi.cloud.utils.StringUtils;
import org.apache.hadoop.io.Text;

public class LetterTotalCount {

    public static class CounterMapper extends Mapper<Object, Text, Text, LongWritable> {
        private final static LongWritable one = new LongWritable(1);
        private final static Text word = new Text("total");

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = StringUtils.normalizeString(value.toString());
            for (char c : line.toCharArray()) {
                String letterStr = Character.toString(Character.toLowerCase(c));
                if (StringUtils.isLetter(letterStr)) {
                        context.write(word, one);
                }
            }
        }    
    }

    public static class CounterReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
        @Override
        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
            LongWritable result = new LongWritable();
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
}