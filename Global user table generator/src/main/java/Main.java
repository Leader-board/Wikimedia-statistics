import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.TreeMap;
import gnu.trove.map.TObjectLongMap;
import gnu.trove.map.hash.*;

public class Main {
    /*
     * Input: a directory that leads to each of the files that we want to combine
     */
    static HashMap<String, TShortIntHashMap> users = new HashMap<>(); // username is key
    static TObjectLongMap<String> reglook = new TObjectLongHashMap<>(); // username -> registration date (if it exists)
    static TShortObjectHashMap<String> wikinamelookup = new TShortObjectHashMap<>();
    static TObjectShortHashMap<String> wikiindexlookup = new TObjectShortHashMap<>();

    static final int buffer_size = 500000000;
    public static void runner(String location, String filename) {
        /*
         * Input: filename to the CSV that will be parsed, and the name itself (which
         * represents the wiki)
         * The CSVs are TAB-FORMATTED
         * https://www.baeldung.com/java-csv-file-array
         */
        int flag = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(location))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (flag == 0) {
                    flag++;
                    continue; // for the headers
                }
                String[] values = line.split("\t");
                String wikiname = filename.split("\\.")[0];
                /*
                 * first: username
                 * second: (if it exists) registration date
                 * third: number of edits
                 */
                if (!values[1].contains("NULL") && !reglook.containsKey(values[0]))
                    reglook.put(values[0], Long.parseLong(values[1]));
                TShortIntHashMap P2 = users.get(values[0]);
                if (P2 == null)
                    P2 = new TShortIntHashMap();
                // check whether wikiname exists
                short index = getwikiindex(wikiname);
                if (index == -1)
                {
                    index = (short) (wikinamelookup.size() + 1);
                    wikinamelookup.put(index, wikiname);
                    wikiindexlookup.put(wikiname, index);
                }
                // add edit count
                if (Integer.parseInt(values[2]) != 0) {
                    P2.put(index, Integer.parseInt(values[2]));
                    users.put(values[0], P2);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    // taken from the internet
    public static void setStream(String f) throws FileNotFoundException {
        File file = new File(f);
        FileOutputStream fos = new FileOutputStream(file);

        // Create new print stream for file.
        PrintStream ps = new PrintStream(fos);

        // Set file print stream.
        System.setOut(ps);
    }
    public static short getwikiindex(String wikiname)
    {
        if (!wikiindexlookup.containsKey(wikiname))
            return -1;
        return wikiindexlookup.get(wikiname);
    }
    public static void generatefulltable(String[] names) throws FileNotFoundException, IOException {
        // full table of edit counts and users, just like an inner JOIN
        // the first line should be just printing them
        // Store console print stream.
        // setStream("C:\\Users\\Leaderboard\\Documents\\fulltable.csv");
        Writer file = new OutputStreamWriter(new FileOutputStream("/vol/bitbucket/dm1321/fulltable.csv"), StandardCharsets.UTF_8);
        BufferedWriter buffer = new BufferedWriter(file, buffer_size);
        buffer.write("Username");
        for (String s : names) {
            // get wiki name
            String wikiname = s.split("\\.")[0];
            buffer.write("|" + wikiname);
        }
        buffer.write("|Total");
        buffer.newLine();
        // now iterate through EVERY USER
        for (String s : reglook.keySet()) {
            buffer.write(s);
            // check whether a user has an edit at a particular wiki
            int contribs = 0;
            TShortIntHashMap hm = users.get(s);
            if (hm != null) {
                for (String t : names) {
                    String wikiname = t.split("\\.")[0];
                    short wikiindex = getwikiindex(wikiname);
                    if (hm.containsKey(wikiindex)) {
                        buffer.write("|" + hm.get(wikiindex));
                        contribs += hm.get(wikiindex);
                    } else
                        buffer.write("|0");
                }
                buffer.write("|" + contribs); // next line
            }
            else
            {
                for (String ignored : names) {
                    buffer.write("|" + 0);
                }
                buffer.write("|" + 0);
            }
            buffer.newLine();
        }
        buffer.flush();
        buffer.close();
    }

    public static void analyser() throws FileNotFoundException, IOException {
        // INPUT: the users and reglook hashmaps that were computed before
        // OUTPUT: a table showing each user's global contribution
        TObjectIntHashMap<String> globalcontribs = new TObjectIntHashMap<>();
        Writer file = new OutputStreamWriter(new FileOutputStream("/vol/bitbucket/dm1321/globalcontribs.csv"), StandardCharsets.UTF_8);
        BufferedWriter buffer = new BufferedWriter(file, buffer_size);
        for (String s : reglook.keySet()) {
            int contribs = 0;
            if (users.containsKey(s)) { // does the user have at least ONE edit?
                for (int i : users.get(s).values()) {
                    contribs += i;
                }
                globalcontribs.put(s, contribs);
            }
            else
            globalcontribs.put(s, 0);
        }
        // now to get them sorted - fairly messy - but sorting a hashmap by value is not
        // easy either...
        TreeMap<Integer, ArrayList<String>> tm = new TreeMap<>((a, b) -> (b - a));
        for (String s : globalcontribs.keySet()) {
            int contribs = globalcontribs.get(s);
            ArrayList<String> arr = tm.get(contribs);
            if (arr == null)
                arr = new ArrayList<>();
            arr.add(s);
            tm.put(contribs, arr);
        }
        // no need to convert back - we can print the result directly
        int rank = 1;
        buffer.write("Rank|Username|Registration_date|Edits");
        buffer.newLine();
        for (int i : tm.keySet()) {
            ArrayList<String> arr = tm.get(i);
            int size = arr.size();
            for (String s : arr) {
                buffer.write(rank + "|" + s + "|" + (reglook.containsKey(s) ? reglook.get(s) : "NULL") + "|" + i);
                buffer.newLine();
            }
            rank += size;
        }
        buffer.flush();
        buffer.close();
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        // list all the files
        // String loc = "\\\\fs-vol-bitbucket.doc.ic.ac.uk\\bitbucket\\dm1321\\test";
        String loc = "/vol/bitbucket/dm1321/wikimedia_update";
        String[] names;
        File f = new File(loc);
        names = f.list();
        assert names != null;
        for (String s : names) {
            System.out.println(loc + "/" + s + " and number of users till then " + users.size() + " with reglook size " + reglook.size() );
            runner(loc + "/" + s, s);
        }
        System.out.println("Generating global contributions table");
        analyser();
        System.out.println("Generating full table matrix");
        generatefulltable(names);
    }
}