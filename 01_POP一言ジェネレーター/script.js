document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('results');

    // キャッチコピー生成テンプレート
    const templates = [
       // --- 第1弾：王道・定番（1-50） ---
  "今夜の食卓に。{name}の{feature}で、大満足。",
  "ひと口で違いがわかる。{name}の{feature}を、今夜。",
  "探していたのはこの味。{name}の{feature}に、脱帽。",
  "食卓がパッと華やぐ。{name}の{feature}が、主役です。",
  "ごちそうは、ここにある。{name}の{feature}で、贅沢時間を。",
  "シンプルに、贅沢に。{name}の{feature}を味わい尽くす。",
  "お箸が止まらない。{name}の{feature}、これぞ本物。",
  "家族の笑顔が見えるはず。{name}の{feature}、いかがですか。",
  "料理がぐんと引き立つ。{name}の{feature}、名脇役です。",
  "今日はこれで決まり。{name}の{feature}が、お腹を満たす。",
  "生産者の顔が見える。{name}の{feature}に、惚れました。",
  "妥協なしの逸品。{name}の{feature}、試してみてください。",
  "下鴨で見つけた宝物。{name}の{feature}を、お届け。",
  "素材の力が溢れてる。{name}の{feature}、そのままで。",
  "手間ひま惜しまぬ味。{name}の{feature}に、心踊る。",
  "職人の技が光る。{name}の{feature}、ここに極まれり。",
  "余計なものは入れない。{name}の{feature}が、体に染みる。",
  "この香りが、証拠です。{name}の{feature}を、食卓へ。",
  "自信を持っておすすめ。{name}の{feature}、間違いなし。",
  "伝統が息づく味。{name}の{feature}に、感謝して。",
  "頑張った自分へのご褒美。{name}の{feature}で、乾杯。",
  "週末の夜を彩る。{name}の{feature}に、酔いしれる。",
  "懐かしいのに、新しい。{name}の{feature}、心に響く。",
  "雨の日も、心は晴れやか。{name}の{feature}、温まる一皿。",
  "大切な人と囲む食卓。{name}の{feature}が、会話を弾ませる。",
  "忙しい夕暮れに。{name}の{feature}が、味方になります。",
  "朝の目覚めが楽しみに。{name}の{feature}、最高の朝食。",
  "旅する気分で味わう。{name}の{feature}、本場を超えた。",
  "ちょっとしたお祝いに。{name}の{feature}、特別を添えて。",
  "季節を先取りする。{name}の{feature}、旬を愛でる。",
  "驚きの{feature}！{name}が、やってきた。",
  "凝縮された{feature}。{name}、解禁。",
  "{name}×{feature}。この組み合わせ、最強。",
  "唸るおいしさ。{name}の{feature}。",
  "究極の{feature}。{name}を、その手に。",
  "魅惑の{feature}、{name}。リピート確定。",
  "まさかの{feature}。{name}、新体験。",
  "{feature}が、止まらない。{name}に夢中。",
  "本気が伝わる、{name}の{feature}。",
  "迷ったら、これ。{name}の{feature}。",
  "知っていましたか？{name}の{feature}の凄さ。",
  "今夜、何食べる？{name}の{feature}にしませんか。",
  "もう戻れないかも。{name}の{feature}を知る前には。",
  "お酒好きのあなたへ。{name}の{feature}が、合いますよ。",
  "お子様もきっと喜ぶ。{name}の{feature}、やさしい味。",
  "素材の甘み、感じてますか？{name}の{feature}で。",
  "いつもの一皿を、格上げ。{name}の{feature}を添えて。",
  "健康を、美味しく。{name}の{feature}が、支えます。",
  "ご飯、おかわり！{name}の{feature}があれば。",
  "フレンドフーズが選んだ、{name}の{feature}。信じてください。",

  // --- 第2弾：信頼・感覚・知恵（51-100） ---
  "私たちが惚れ込んだ。{name}の{feature}に、納得。",
  "ついに見つけました。{name}の{feature}、本物です。",
  "毎日食べたい理由がある。{name}の{feature}を、食卓に。",
  "目利きが選ぶ一品。{name}の{feature}、試さなきゃ損。",
  "嘘のない、まっすぐな味。{name}の{feature}に、感動。",
  "隠れた名品を、下鴨で。{name}の{feature}、見逃せません。",
  "ずっと守りたい日本の味。{name}の{feature}に、癒やされる。",
  "胸を張ってお出しします。{name}の{feature}、最高。",
  "期待を裏切らない。{name}の{feature}、一度食べてみて。",
  "フレンドフーズの看板娘。{name}の{feature}、愛されてます。",
  "鼻を抜ける芳醇な香り。{name}の{feature}に、うっとり。",
  "シャキッと、じゅわっと。{name}の{feature}、弾ける。",
  "黄金色に輝く。{name}の{feature}、目でも楽しんで。",
  "噛みしめるほどに。{name}の{feature}、旨み溢れる。",
  "とろけるような口溶け。{name}の{feature}、至福の時。",
  "優しい甘みが広がります。{name}の{feature}、心まで。",
  "この食感、クセになる。{name}の{feature}、新感覚。",
  "出汁の深みに驚くはず。{name}の{feature}、滋味。",
  "色鮮やかに、食卓を。{name}の{feature}、芸術。",
  "パチパチと音が聞こえる。{name}の{feature}、出来たての味。",
  "仕上げにひと振り。{name}の{feature}で、プロの味。",
  "冷めても美味しい。{name}の{feature}、お弁当の主役に。",
  "忙しい朝の救世主。{name}の{feature}で、栄養満点。",
  "お豆腐に乗せるだけ。{name}の{feature}、魔法のひと手間。",
  "白ごはんに寄り添う。{name}の{feature}、最高の相棒。",
  "パン派のあなたにも。{name}の{feature}、意外な相性。",
  "野菜嫌いの子も喜ぶ。{name}の{feature}、秘密のレシピ。",
  "余韻まで楽しむ。{name}の{feature}、食後のひととき。",
  "お持たせにも喜ばれる。{name}の{feature}、褒められギフト。",
  "献立に迷ったら、これ。{name}の{feature}が、解決します。",
  "スーパーの域を超えた。{name}の{feature}、驚きを。",
  "歴史が物語るおいしさ。{name}の{feature}、深いです。",
  "100年後も残したい。{name}の{feature}、日本の誇り。",
  "実は、これだけなんです。{name}の{feature}、究極の引き算。",
  "食べるサプリメント。{name}の{feature}で、体メンテナンス。",
  "毎日がもっと楽しくなる。{name}の{feature}がある暮らし。",
  "下鴨の空気に馴染む。{name}の{feature}、やさしい味。",
  "教えたくない、自分だけの。{name}の{feature}、独り占め。",
  "開けた瞬間、魔法にかかる。{name}の{feature}。",
  "今日一日のご褒美に。{name}の{feature}を、ゆっくりと。",
  "凝縮、{name}の{feature}。",
  "圧巻の、{name}の{feature}。",
  "直撃、{name}の{feature}。",
  "虜になる。{name}の{feature}。",
  "正解は、{name}の{feature}でした。",
  "逸脱。{name}の{feature}。",
  "納得の、{name}の{feature}。",
  "必然。{name}の{feature}との出会い。",
  "珠玉、{name}の{feature}。",
  "これが、フレンドフーズの{name}の{feature}。",

  // --- 第3弾：エッジ・知性・無重力（101-150） ---
  "覚悟してください。{name}の{feature}で、価値観が変わります。",
  "スーパーの棚に並ぶ奇跡。{name}の{feature}に、ひれ伏す。",
  "流行りは追いかけません。{name}の{feature}、これが正解。",
  "0か100か。{name}の{feature}、好きな人は一生離れられない。",
  "宣伝不要。{name}の{feature}、わかる人にだけ届け。",
  "もはや狂気。{name}の{feature}、ここまでのこだわりが必要か。",
  "効率？無視しました。{name}の{feature}、ただ旨さのために。",
  "「たかが{name}」なんて言わせない。{feature}、圧倒的です。",
  "他とは比べないで。{name}の{feature}、孤高の存在。",
  "下鴨の基準は、ここにある。{name}の{feature}。",
  "皿の上の文化財。{name}の{feature}、深く味わう。",
  "理由のない美味しさはない。{name}の{feature}、その裏側。",
  "400年の歴史が、この一袋に。{name}の{feature}。",
  "科学的に説明できない幸福感。{name}の{feature}。",
  "素材への冒涜を一切禁じた。{name}の{feature}。",
  "文豪も愛したかもしれない。{name}の{feature}に、想いを馳せて。",
  "伝統とは、守るものではなく磨くもの。{name}の{feature}。",
  "その一口は、土地の記憶。{name}の{feature}。",
  "発酵の芸術。{name}の{feature}、時間が生んだ奇跡。",
  "美味は、細部に宿る。{name}の{feature}。",
  "夕暮れの下鴨、{name}の{feature}を抱えて帰る幸せ。",
  "騒がしい日常を、{name}の{feature}が、静める。",
  "明日への活力を、{name}の{feature}で充電する。",
  "この味が、故郷になる。{name}の{feature}。",
  "誰にも教えたくない、秘密の贅沢。{name}の{feature}。",
  "雨の日も、心は晴れやか。{name}の{feature}が、さらっていく。",
  "懐かしさは、未来への約束。{name}の{feature}。",
  "言葉はいらない。{name}の{feature}、ただただ美味しい。",
  "季節が、足音を立ててやってくる。{name}の{feature}と共に。",
  "頑張った魂を癒やす、{name}の{feature}。",
  "思考が浮遊する。{name}の{feature}、異次元の旨さ。",
  "重力からの解放。{name}の{feature}、軽やかな口溶け。",
  "胃袋が、宇宙になる。{name}の{feature}を満たして。",
  "常識を逆さまにする。{name}の{feature}、衝撃の体験。",
  "時空を超える美味しさ。{name}の{feature}。",
  "箸が、勝手に吸い寄せられる。{name}の{feature}の重力。",
  "夢か、現か。{name}の{feature}、幻の味わい。",
  "食卓の引力が変わる。{name}の{feature}が、中心。",
  "浮き足立つほどに、旨い。{name}の{feature}。",
  "物理法則を無視した、{name}の{feature}。",
  "本物を知る勇気はあるか。{name}の{feature}。",
  "これを食べずに、{name}を語るなかれ。{feature}、必見。",
  "驚かない人はいない。{name}の{feature}、その衝撃に備えて。",
  "後戻りはできません。{name}の{feature}の虜になる。",
  "一口で、世界が変わる音がした。{name}の{feature}。",
  "禁断の果実のような。{name}の{feature}、解禁。",
  "限界突破。{name}の{feature}、常識の外へ。",
  "偽物には、もう戻れない。{name}の{feature}。",
  "あなたの五感を、再起動する。{name}の{feature}。",
  "フレンドフーズからの、挑戦状。{name}の{feature}、どう思う？",

  // --- 第4弾：偏愛・京都・哲学（151-200） ---
  "私の給料、これに消えてます。{name}の{feature}。",
  "会議で揉めました。でも、この{name}の{feature}だけは譲れない。",
  "3日間、これのことしか考えられなかった。{name}の{feature}。",
  "誰にも教えたくない、スタッフだけの秘密。{name}の{feature}。",
  "寝ても覚めても、{name}の{feature}。",
  "これを置かない店は、フレンドフーズじゃない。{name}の{feature}。",
  "頼むから、一口だけでいい。{name}の{feature}を食べてくれ。",
  "喉が鳴る。{name}の{feature}、その背徳感。",
  "胃袋へのラブレター。{name}の{feature}。",
  "完売御礼の予感。{name}の{feature}、早い者勝ち。",
  "下鴨の夜は、{name}の{feature}で更けていく。",
  "鴨川のせせらぎ、{name}の{feature}。",
  "京都の「美味しい」の基準を、塗り替える。{name}の{feature}。",
  "凛とした、{name}の{feature}。これぞ京の底力。",
  "華やかさの裏に、本質がある。{name}の{feature}。",
  "お公家さんも驚く。{name}の{feature}、現代の贅。",
  "糺の森の静寂に似た、{name}の{feature}。",
  "この地で愛されて、磨かれた。{name}の{feature}。",
  "京都人が最後に辿り着く。{name}の{feature}。",
  "フレンドフーズが、下鴨の台所である理由。{name}の{feature}。",
  "食事は、自分への一番の投資。{name}の{feature}。",
  "身体は、食べたものでできている。{name}の{feature}を。",
  "贅沢とは、高いことじゃない。{name}の{feature}を知ることだ。",
  "孤独な夜も、{name}の{feature}があれば大丈夫。",
  "人生最後に何食べる？私は{name}の{feature}。",
  "胃袋を満たし、心まで洗う。{name}の{feature}。",
  "丁寧な暮らしは、この{name}の{feature}から。",
  "絶望さえも、{name}の{feature}が、希望に変える。",
  "食べることは、生きることへの賛歌。{name}の{feature}。",
  "昨日の自分より、美味しいものを。{name}の{feature}。",
  "浮き世を忘れる。{name}の{feature}、夢心地。",
  "脳内麻薬、{name}の{feature}。",
  "五感が無重力状態。{name}の{feature}。",
  "現実逃避のお供に。{name}の{feature}。",
  "銀河系で一番、{name}の{feature}。",
  "引力に抗う、この{name}の{feature}。",
  "意識が飛ぶ。{name}の{feature}、その衝撃。",
  "四次元の味わい。{name}の{feature}。",
  "魂が、宙に舞う。{name}の{feature}で。",
  "重力を忘れて、味わい尽くせ。{name}の{feature}。",
  "{name}、すなわち、{feature}。",
  "黙って、{name}の{feature}。",
  "唯一無二、{name}の{feature}。",
  "{name}、震撼。",
  "猛烈に、{name}。",
  "究極、ここに。{name}の{feature}。",
  "美味の臨界点。{name}の{feature}。",
  "正真正銘。{name}の{feature}。",
  "異次元への扉。{name}の{feature}。",
  "フレンドフーズ、渾身。{name}の{feature}。"
    ];

    generateBtn.addEventListener('click', () => {
        const productName = document.getElementById('productName').value.trim();
        const featuresInput = document.getElementById('features').value.trim();

        if (!productName || !featuresInput) {
            alert('商品名と特徴を入力してください！');
            return;
        }

        // 特徴をスペース、カンマ、読点で分割して配列にする
        const featuresList = featuresInput.split(/[\s,、]+/).filter(f => f.length > 0);
        const feature = featuresList[Math.floor(Math.random() * featuresList.length)];

        // UIリセット
        resultSection.style.display = 'block';
        loading.style.display = 'block';
        resultsContainer.innerHTML = '';

        // AI風の遅延演出
        setTimeout(() => {
            loading.style.display = 'none';
            generateCatchphrases(productName, featuresList);
        }, 1500);
    });

    function generateCatchphrases(name, featuresList) {
        // ランダムに3つ選ぶ
        const shuffled = templates.sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 3);

        selected.forEach(template => {
            // それぞれのキャッチコピーでランダムな特徴を使う
            const feature = featuresList[Math.floor(Math.random() * featuresList.length)];
            const catchphrase = template
                .replace(/{name}/g, name)
                .replace(/{feature}/g, feature);

            const card = document.createElement('div');
            card.className = 'pop-card';
            card.textContent = catchphrase;
            resultsContainer.appendChild(card);
        });
    }
});
