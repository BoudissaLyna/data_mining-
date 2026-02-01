#  The Ouedkniss Laptop Journey: Our Quest for Price Logic
 

---

##  Phase 1: Problem Framing (Our Motivation)
When we first started this project, we asked ourselves: *"Why is it so hard to find a fair price for a laptop in Algeria?"*  

The Ouedkniss marketplace is a digital jungle. Prices fluctuate wildly based on seller mood, urgent needs, and unstandardized specs. We decided to take on the challenge of **decoding this market**. 

**Our Goal:** To build an AI model that doesn't just guess a number, but understands the *market tier* of a laptop based on its guts (RAM, CPU, Screen, and Storage). We chose **Classification** over simple Regression because we realized that in Algeria, laptops exist in "Market Identities" (e.g., "The Student Budget" vs "The Gamer's Choice").

---

##  Phase 2: Data Collection & The Great Integration
Our journey began with a massive pull of **66,667 raw listings**.  

**What we did:**
1.  **Unified our Front:** We each took a part of the specs. Lyna handled the core identities (Brand/Price), Aya focused on the visual impact (Screens), Leena looked at the long-term memory (Storage), and Abdallah  Mimoun validated the brainpower (CPU/GPU).
2.  **The "Unknown" Battle:** The raw data was full of placeholders like *"NeedToBeFilled"* or *"Prochainement"*. Instead of just deleting everything, we cross-referenced. If a laptop said 'i7-12700H', we *knew* what it was even if the seller didn't fill the CPU TIER column.
3.  **The Master Merge:** We integrated these separate findings into one 'Master Cleaned Dataset'. We ended up with **~42,000 pristine records**, having filtered out the "garbage" (laptops priced at 1 DZD or 999,999,999 DZD).

---

##  Phase 3: Feature Engineering (Speaking the AI's Language)
We didn't just throw raw numbers at the model. We engineered new "logic features":
-   **PPI & Total Pixels:** Because a clear screen is worth more.
-   **Storage Score:** We weighted SSD 5x more than HDD, reflecting real-world speed preferences.
-   **Gaming Flags:** We scanned model names for keywords like 'ROG' or 'Legion' to catch that premium "Gamer Tax" value.

---

##  Phase 4: Our Modeling Strategy
This is where we made our biggest strategic choice. We ran a competition between two splitting philosophies: **Gini Index** and **Entropy**.

**Our Strategic Decisions:**
-   **The Bias-Variance Tradeoff:** We noticed that a tree with Depth 35 had the "highest" accuracy (~77.04%), but it looked like it was memorizing specific sellers.
-   **The Pruning Victory:** We decided to stop at **Depth 25**. Why? Because we wanted a model that works for a *new* laptop posted tomorrow, not just for the ones we collected yesterday.
-   **The Winner:** Gini Index at Depth 25 gave us **76.85% Accuracy**. It's stable, it's fast, and it understands the difference between a "Standard" laptop and a "Premium" beast almost 8 times out of 10.

---

##  Final Verdict
Our project proved that even in a chaotic market like Ouedkniss, there is a hidden logic. By focusing on **Categorical Tiers** and using **Strategic Pruning**, we've built a tool that acts as a digital advisor for the Algerian laptop market.

