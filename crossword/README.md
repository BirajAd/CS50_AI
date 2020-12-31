This problem is from one of the projects in CS50 AI program taugh by Harvard University.

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python generate.py data/structure1.txt data/words1.txt output.png

██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
</code></pre></div></div>

The code in the project has to do with solving a crossword puzzle.Every empty slot in the crossword to be filled by word are represented by class <code class="language-plaintext highlighter-rouge">Variable</code>. Variable has property <code class="language-plaintext highlighter-rouge">i</code>, <code class="language-plaintext highlighter-rouge">j</code>, <code class="language-plaintext highlighter-rouge">direction</code>, and <code class="language-plaintext highlighter-rouge">length</code>. <code class="language-plaintext highlighter-rouge">i</code> and <code class="language-plaintext highlighter-rouge">j</code> represent the position of the letter, <code class="language-plaintext highlighter-rouge">direction</code> shows whether the word's direction is <code class="language-plaintext highlighter-rouge">down</code> or <code class="language-plaintext highlighter-rouge">across</code> and <code class="language-plaintext highlighter-rouge">length</code> is the length of the slot. Every <code class="language-plaintext highlighter-rouge">Variable</code> are assigned words from domain and it later gets filtered by its length with <code class="language-plaintext highlighter-rouge">enforce_node_consistency()</code> function. The problem is solved using <code class="language-plaintext highlighter-rouge">backtrack</code> and <code class="language-plaintext highlighter-rouge">ac3</code> algorithm.

<code class="language-plaintext highlighter-rouge">data/wordsX.txt</code> file contains words that can be used for puzzle with structure as of <code class="language-plaintext highlighter-rouge">data/structureX.txt</code> file

Some Python libraries like Pillow are used in the project to generate image of the crossword. it can be installed by executing <code class="language-plaintext highlighter-rouge">pip3 install Pillow</code>
