import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.TreeMap;

public class Main {
    /*
     * Input: a directory that leads to each of the files that we want to combine
     */
    static HashMap<String, HashMap<String, Integer>> users = new HashMap<>(); // username is key
    static HashMap<String, Long> reglook = new HashMap<>(); // username -> registration date (if it exists)
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
                if (!values[1].contains("NULL"))
                    reglook.put(values[0], Long.parseLong(values[1]));
                HashMap<String, Integer> P2 = users.get(values[0]);
                if (P2 == null)
                    P2 = new HashMap<>();
                // add edit count
                P2.put(wikiname, Integer.parseInt(values[2]));
                users.put(values[0], P2);
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

    public static void generatefulltable(String[] names) throws FileNotFoundException {
        // full table of edit counts and users, just like an inner JOIN
        // the first line should be just printing them
        // Store console print stream.
        setStream("/vol/bitbucket/dm1321/fulltable.csv");
        System.out.print("Username");
        for (String s : names) {
            // get wiki name
            String wikiname = s.split("\\.")[0];
            System.out.print("|" + wikiname);
        }
        System.out.println("|Total");
        // now iterate through EVERY USER
        for (String s : users.keySet()) {
            System.out.print(s);
            // check whether a user has an edit at a particular wiki
            int contribs = 0;
            HashMap<String, Integer> hm = users.get(s);
            for (String t : names) {
                String wikiname = t.split("\\.")[0];
                if (hm.containsKey(wikiname)) {
                    System.out.print("|" + hm.get(wikiname));
                    contribs += hm.get(wikiname);
                } else
                    System.out.print("|0");
            }
            System.out.println("|" + contribs); // next line
        }
    }

    public static void analyser() throws FileNotFoundException {
        // INPUT: the users and reglook hashmaps that were computed before
        // OUTPUT: a table showing each user's global contribution
        setStream("/vol/bitbucket/dm1321/globalcontribs.csv");
        HashMap<String, Integer> globalcontribs = new HashMap<>();
        for (String s : users.keySet()) {
            int contribs = 0;
            for (int i : users.get(s).values()) {
                contribs += i;
            }
            globalcontribs.put(s, contribs);
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
        System.out.println("Rank|Username|Registration_date|Edits");
        for (int i : tm.keySet()) {
            ArrayList<String> arr = tm.get(i);
            int size = arr.size();
            for (String s : arr) {
                System.out.println(rank + "|" + s + "|" + (reglook.containsKey(s) ? reglook.get(s) : "NULL") + "|" + i);
            }
            rank += size;
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        // list all the files
        // String loc = "\\\\fs-vol-bitbucket.doc.ic.ac.uk\\bitbucket\\dm1321\\test";
        String loc = "/vol/bitbucket/dm1321/wikimedia/Raw CSV data";
        String[] names;
        File f = new File(loc);
        names = f.list();
        assert names != null;
        for (String s : names) {
            // System.out.println(loc + "/" + s);
            runner(loc + "/" + s, s);
        }
        analyser();
        generatefulltable(names);
    }
}
