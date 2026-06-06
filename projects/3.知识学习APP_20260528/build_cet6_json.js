// 从 docx 提取的原始词表构建 english_cet6.json，并注入习题
const fs = require('fs');

// 1. Read raw words from PowerShell extraction
let rawStr = fs.readFileSync(
  'E:/.Claude Code Project/3.知识学习APP_20260528/cet6_words_raw.json', 'utf8'
);
if (rawStr.charCodeAt(0) === 0xFEFF) rawStr = rawStr.slice(1);
const rawWords = JSON.parse(rawStr);

// 2. Quiz data — inline QUIZ_MAP for 75 CET6 core words

const QUIZ_MAP = {
  abandon: [{ id:"cet6_q_abandon", type:"single_choice", question:"The captain gave the order to ______ ship when the fire spread beyond control.", options:[{key:"A",text:"abolish"},{key:"B",text:"abandon"},{key:"C",text:"absorb"},{key:"D",text:"abuse"}], answer:"B", explanation:"abandon ship 为固定搭配，意为'弃船'。abolish（废除法律/制度）、absorb（吸收）、abuse（滥用/虐待）均不适用于'离开危险船只'的语境。" }],
  abolish: [{ id:"cet6_q_abolish", type:"single_choice", question:"Slavery was ______ in the United States in 1865 with the ratification of the 13th Amendment.", options:[{key:"A",text:"abandoned"},{key:"B",text:"abolished"},{key:"C",text:"absorbed"},{key:"D",text:"accelerated"}], answer:"B", explanation:"abolish 专门指'废除法律、制度或习俗'，与 slavery（奴隶制）搭配最恰当。abandon（放弃具体事物）不涉及制度层面的废除。absorb（吸收）和 accelerate（加速）均不符合句意。" }],
  abnormal: [{ id:"cet6_q_abnormal", type:"single_choice", question:"The doctor ordered more tests after noticing ______ levels of white blood cells in the patient.", options:[{key:"A",text:"normal"},{key:"B",text:"abnormal"},{key:"C",text:"informal"},{key:"D",text:"enormous"}], answer:"B", explanation:"abnormal levels = 异常水平。normal（正常的）与句意相反，informal（非正式的）、enormous（巨大的）语义不匹配。" }],
  abrupt: [{ id:"cet6_q_abrupt", type:"single_choice", question:"The meeting came to an ______ end when the CEO stood up and walked out without a word.", options:[{key:"A",text:"abrupt"},{key:"B",text:"abstract"},{key:"C",text:"absurd"},{key:"D",text:"absolute"}], answer:"A", explanation:"abrupt end = 突然结束。abstract（抽象的）、absurd（荒谬的）、absolute（绝对的）均不修饰'结束方式'。" }],
  absorb: [{ id:"cet6_q_absorb", type:"single_choice", question:"Plants ______ carbon dioxide from the atmosphere and release oxygen through photosynthesis.", options:[{key:"A",text:"absorb"},{key:"B",text:"abolish"},{key:"C",text:"abandon"},{key:"D",text:"abuse"}], answer:"A", explanation:"absorb = 吸收，是植物光合作用的科学描述。abolish（废除）、abandon（放弃）、abuse（滥用）均与生物过程无关。" }],
  abstract: [{ id:"cet6_q_abstract", type:"single_choice", question:"Justice and freedom are ______ concepts that are difficult to define in concrete terms.", options:[{key:"A",text:"concrete"},{key:"B",text:"abstract"},{key:"C",text:"absolute"},{key:"D",text:"accurate"}], answer:"B", explanation:"abstract concept = 抽象概念，与'difficult to define in concrete terms（难以用具体术语定义）'呼应。concrete（具体的）是反义词，absolute（绝对的）、accurate（精确的）不匹配。" }],
  absurd: [{ id:"cet6_q_absurd", type:"single_choice", question:"It's ______ to blame the weather for your poor exam performance.", options:[{key:"A",text:"abrupt"},{key:"B",text:"absurd"},{key:"C",text:"abstract"},{key:"D",text:"accurate"}], answer:"B", explanation:"absurd = 荒谬的，指'把考试差归咎于天气'这种逻辑是荒谬的。abrupt（突然的）、abstract（抽象的）、accurate（精确的）均不表示'不合逻辑的'。" }],
  abundant: [{ id:"cet6_q_abundant", type:"single_choice", question:"The region has ______ supplies of fresh water, making it ideal for agriculture.", options:[{key:"A",text:"abnormal"},{key:"B",text:"absurd"},{key:"C",text:"abundant"},{key:"D",text:"accurate"}], answer:"C", explanation:"abundant supplies = 充足的供应。abnormal（反常的）、absurd（荒谬的）、accurate（精确的）语义不匹配。" }],
  abuse: [{ id:"cet6_q_abuse", type:"single_choice", question:"The official was dismissed for ______ his authority to award contracts to his relatives.", options:[{key:"A",text:"using"},{key:"B",text:"abusing"},{key:"C",text:"abandoning"},{key:"D",text:"absorbing"}], answer:"B", explanation:"abuse one's authority = 滥用职权，是固定搭配。使用use（使用）没有贬义，abandon（放弃）和 absorb（吸收）不适用于权力滥用场景。" }],
  accelerate: [{ id:"cet6_q_accelerate", type:"single_choice", question:"The government hopes tax cuts will ______ economic recovery.", options:[{key:"A",text:"abolish"},{key:"B",text:"accelerate"},{key:"C",text:"accompany"},{key:"D",text:"accumulate"}], answer:"B", explanation:"accelerate economic recovery = 加速经济复苏。abolish（废除）、accompany（陪伴）、accumulate（积累）均不与'recovery'构成合理的动宾搭配。" }],
  access: [{ id:"cet6_q_access", type:"single_choice", question:"Only employees with security clearance have ______ to the confidential database.", options:[{key:"A",text:"access"},{key:"B",text:"excess"},{key:"C",text:"accent"},{key:"D",text:"accident"}], answer:"A", explanation:"have access to = 有权使用/进入，是固定搭配。excess（过量）、accent（口音）、accident（事故）均不表示'权限'。" }],
  accommodation: [{ id:"cet6_q_accommodation", type:"single_choice", question:"Finding affordable ______ near campus is the biggest challenge for exchange students.", options:[{key:"A",text:"accommodation"},{key:"B",text:"recommendation"},{key:"C",text:"administration"},{key:"D",text:"qualification"}], answer:"A", explanation:"accommodation = 住宿，留学场景下最核心的需求。recommendation（推荐信）、administration（行政管理）、qualification（资格）语义不匹配。" }],
  accompany: [{ id:"cet6_q_accompany", type:"single_choice", question:"High fever is usually ______ by a headache and body aches.", options:[{key:"A",text:"accompanied"},{key:"B",text:"accomplished"},{key:"C",text:"accumulated"},{key:"D",text:"accelerated"}], answer:"A", explanation:"be accompanied by = 由…伴随，指'高烧伴随头痛'这种伴发症状关系。accomplished（完成）、accumulated（积累）、accelerated（加速）均不能表示'伴随'。" }],
  accomplish: [{ id:"cet6_q_accomplish", type:"single_choice", question:"After months of hard work, the team finally ______ its mission ahead of schedule.", options:[{key:"A",text:"abandoned"},{key:"B",text:"accomplished"},{key:"C",text:"accompanied"},{key:"D",text:"accumulated"}], answer:"B", explanation:"accomplish one's mission = 完成任务。abandon（放弃）与句意相反，accompany（陪伴）、accumulate（积累）不匹配。" }],
  accumulate: [{ id:"cet6_q_accumulate", type:"single_choice", question:"Over the past decade, the investor has ______ a fortune worth more than 500 million dollars.", options:[{key:"A",text:"accumulated"},{key:"B",text:"accelerated"},{key:"C",text:"accomplished"},{key:"D",text:"accompanied"}], answer:"A", explanation:"accumulate a fortune = 积累财富，指长期、逐步地积聚财富。accelerate（加速）、accomplish（完成）、accompany（陪伴）均不描述财富的'积累过程'。" }],
  accurate: [{ id:"cet6_q_accurate", type:"single_choice", question:"Weather forecasts are becoming more ______ thanks to advances in satellite technology.", options:[{key:"A",text:"absurd"},{key:"B",text:"accurate"},{key:"C",text:"abrupt"},{key:"D",text:"adequate"}], answer:"B", explanation:"accurate forecasts = 准确的预报。absurd（荒谬的）、abrupt（突然的）、adequate（足够的）不符合'精确性'要求。" }],
  accuse: [{ id:"cet6_q_accuse", type:"single_choice", question:"The journalist was ______ of fabricating sources in several of her investigative reports.", options:[{key:"A",text:"accused"},{key:"B",text:"acquired"},{key:"C",text:"accessed"},{key:"D",text:"adjusted"}], answer:"A", explanation:"be accused of = 被指控，固定搭配。acquired（获得）、accessed（访问）、adjusted（调整）均不能与'of'构成固定搭配。" }],
  acknowledge: [{ id:"cet6_q_acknowledge", type:"single_choice", question:"The CEO finally ______ that the company had made serious errors in handling customer data.", options:[{key:"A",text:"acquired"},{key:"B",text:"abandoned"},{key:"C",text:"acknowledged"},{key:"D",text:"accomplished"}], answer:"C", explanation:"acknowledge that = 承认某事。acquire（获得）、abandon（放弃）、accomplish（完成）均不表示'承认'的动作。" }],
  acquaint: [{ id:"cet6_q_acquaint", type:"single_choice", question:"New employees must take time to ______ themselves with the company's safety regulations.", options:[{key:"A",text:"acquaint"},{key:"B",text:"acquire"},{key:"C",text:"accuse"},{key:"D",text:"acknowledge"}], answer:"A", explanation:"acquaint oneself with = 使自己熟悉，固定搭配。acquire（获得/学到）、accuse（指控）、acknowledge（承认）均不能与'oneself with'构成固定用法。" }],
  acquire: [{ id:"cet6_q_acquire", type:"single_choice", question:"Living in London for three years helped her ______ near-native fluency in English.", options:[{key:"A",text:"accuse"},{key:"B",text:"acquire"},{key:"C",text:"acquaint"},{key:"D",text:"acknowledge"}], answer:"B", explanation:"acquire fluency = 获得/掌握流利度，指通过生活经验习得语言能力。accuse（指控）、acquaint（使熟悉，需加oneself with）、acknowledge（承认）语义和搭配均不正确。" }],
  adequate: [{ id:"cet6_q_adequate", type:"single_choice", question:"Without ______ preparation, students are unlikely to pass the challenging entrance examination.", options:[{key:"A",text:"accurate"},{key:"B",text:"absurd"},{key:"C",text:"adequate"},{key:"D",text:"abstract"}], answer:"C", explanation:"adequate preparation = 充分准备。accurate（精确的）、absurd（荒谬的）、abstract（抽象的）均不修饰'preparation'。" }],
  adjust: [{ id:"cet6_q_adjust", type:"single_choice", question:"It's normal to need some time to ______ to the fast pace of university life.", options:[{key:"A",text:"adjust"},{key:"B",text:"accuse"},{key:"C",text:"acquire"},{key:"D",text:"acknowledge"}], answer:"A", explanation:"adjust to = 适应，固定搭配。'adjust to university life' 是常见语境。accuse（指控）、acquire（获得）、acknowledge（承认）均不能与'to'构成'适应'的含义。" }],
  administration: [{ id:"cet6_q_administration", type:"single_choice", question:"The new ______ has promised to reduce taxes and increase public spending on education.", options:[{key:"A",text:"administration"},{key:"B",text:"accommodation"},{key:"C",text:"recommendation"},{key:"D",text:"qualification"}], answer:"A", explanation:"administration = 政府/行政当局。accommodation（住宿）、recommendation（推荐）、qualification（资格）均不用于描述政府。" }],
  bankrupt: [{ id:"cet6_q_bankrupt", type:"single_choice", question:"After years of falling sales, the century-old department store went ______ and closed all its branches.", options:[{key:"A",text:"bankrupt"},{key:"B",text:"abrupt"},{key:"C",text:"abundant"},{key:"D",text:"abstract"}], answer:"A", explanation:"go bankrupt = 破产，固定搭配。abrupt（突然的）、abundant（丰富的）、abstract（抽象的）均不用于描述'公司财务崩溃'。" }],
  bargain: [{ id:"cet6_q_bargain", type:"single_choice", question:"The antique vase was a real ______ at just 50 dollars — it's worth at least 200.", options:[{key:"A",text:"burden"},{key:"B",text:"bargain"},{key:"C",text:"budget"},{key:"D",text:"barrier"}], answer:"B", explanation:"a real bargain = 真便宜货，指物超所值的交易。burden（负担）、budget（预算）、barrier（障碍）均不表示'便宜货'。" }],
  betray: [{ id:"cet6_q_betray", type:"single_choice", question:"The spy was executed for ______ his country by selling military secrets to the enemy.", options:[{key:"A",text:"betraying"},{key:"B",text:"bargaining"},{key:"C",text:"blaming"},{key:"D",text:"beating"}], answer:"A", explanation:"betray one's country = 背叛国家，与'selling military secrets（出卖军事机密）'相对应。bargaining（讨价还价）、blaming（责备）、beating（打败）与'叛国'无关。" }],
  calculate: [{ id:"cet6_q_calculate", type:"single_choice", question:"Scientists have ______ that the asteroid will pass within 2 million miles of Earth.", options:[{key:"A",text:"calculated"},{key:"B",text:"campaigned"},{key:"C",text:"captured"},{key:"D",text:"canceled"}], answer:"A", explanation:"calculate = 计算/估算，指科学家通过数据计算出小行星的飞越距离。campaign（参加运动）、capture（捕获）、cancel（取消）均不适用于'科学计算'场景。" }],
  campaign: [{ id:"cet6_q_campaign", type:"single_choice", question:"The organization has launched a nationwide ______ to promote recycling and reduce plastic waste.", options:[{key:"A",text:"campaign"},{key:"B",text:"company"},{key:"C",text:"campus"},{key:"D",text:"concept"}], answer:"A", explanation:"launch a campaign = 发起一场运动，指全国性的环保宣传活动。company（公司）、campus（校园）、concept（概念）均不能用'launch'搭配。" }],
  capable: [{ id:"cet6_q_capable", type:"single_choice", question:"With proper training, most people are ______ of learning basic first-aid skills.", options:[{key:"A",text:"capable"},{key:"B",text:"accurate"},{key:"C",text:"adequate"},{key:"D",text:"absurd"}], answer:"A", explanation:"be capable of = 有能力做某事，固定搭配。accurate（精确的）、adequate（足够的）、absurd（荒谬的）均不能用于'be + adj + of + doing'结构。" }],
  colleague: [{ id:"cet6_q_colleague", type:"single_choice", question:"Dr. Wang and her ______ at the research institute have been working on the vaccine for over two years.", options:[{key:"A",text:"companions"},{key:"B",text:"colleagues"},{key:"C",text:"customers"},{key:"D",text:"clients"}], answer:"B", explanation:"colleagues = 同事/同僚，指同一研究机构的专业人员。companions（同伴，偏社交陪伴）、customers（顾客）、clients（客户）均不表示职业合作关系。" }],
  comprehensive: [{ id:"cet6_q_comprehensive", type:"single_choice", question:"Before making a career decision, you should conduct a ______ review of all available options.", options:[{key:"A",text:"complicated"},{key:"B",text:"comprehensive"},{key:"C",text:"conservative"},{key:"D",text:"competitive"}], answer:"B", explanation:"comprehensive review = 全面审视。complicated（复杂的）、conservative（保守的）、competitive（有竞争力的）均不表示'全面的、详尽的'。" }],
  deadline: [{ id:"cet6_q_deadline", type:"single_choice", question:"The project team worked overtime every day to meet the ______ set by the client.", options:[{key:"A",text:"headline"},{key:"B",text:"deadline"},{key:"C",text:"baseline"},{key:"D",text:"airline"}], answer:"B", explanation:"meet the deadline = 赶上截止日期，是项目管理最常用短语。headline（新闻标题）拼写相近但含义完全不同。" }],
  deliberate: [{ id:"cet6_q_deliberate", type:"single_choice", question:"The fire was not an accident — investigators concluded it was a ______ act of sabotage.", options:[{key:"A",text:"delicate"},{key:"B",text:"deliberate"},{key:"C",text:"desperate"},{key:"D",text:"dramatic"}], answer:"B", explanation:"deliberate act = 蓄意行为，与'not an accident（并非意外）'对应。delicate（精致的）、desperate（绝望的）、dramatic（戏剧性的）均不表示'故意的'。" }],
  demonstrate: [{ id:"cet6_q_demonstrate", type:"single_choice", question:"The study clearly ______ that regular exercise can significantly reduce the risk of heart disease.", options:[{key:"A",text:"demonstrates"},{key:"B",text:"distributes"},{key:"C",text:"dominates"},{key:"D",text:"donates"}], answer:"A", explanation:"demonstrate = 证明，指科学研究'证明'了运动对健康的益处。distribute（分配）、dominate（主导）、donate（捐赠）语义不匹配。" }],
  distinguish: [{ id:"cet6_q_distinguish", type:"single_choice", question:"To be a good art critic, you need to be able to ______ genuine masterpieces from skilled imitations.", options:[{key:"A",text:"distinguish"},{key:"B",text:"distribute"},{key:"C",text:"demonstrate"},{key:"D",text:"eliminate"}], answer:"A", explanation:"distinguish A from B = 区分A和B，指鉴赏能力。distribute（分配）、demonstrate（证明）、eliminate（消除）语义不匹配。" }],
  domestic: [{ id:"cet6_q_domestic", type:"single_choice", question:"GDP growth slowed due to weak ______ demand, although exports remained strong.", options:[{key:"A",text:"domestic"},{key:"B",text:"dramatic"},{key:"C",text:"dominant"},{key:"D",text:"distant"}], answer:"A", explanation:"domestic demand = 国内需求，与'exports（出口）'形成内外对比。dramatic（戏剧性的）、dominant（占主导的）、distant（遥远的）均不能与'exports'对照表示'国内市场'。" }],
  eliminate: [{ id:"cet6_q_eliminate", type:"single_choice", question:"The new screening system is designed to ______ candidates who lack basic communication skills.", options:[{key:"A",text:"elevate"},{key:"B",text:"eliminate"},{key:"C",text:"embrace"},{key:"D",text:"employ"}], answer:"B", explanation:"eliminate = 淘汰/筛除，指筛选系统中'淘汰'不合格人选。elevate（提升）、embrace（拥抱/接纳）、employ（雇用）与筛选淘汰的语境相反或无关。" }],
  embrace: [{ id:"cet6_q_embrace", type:"single_choice", question:"Unlike traditional industries, tech companies were quick to ______ remote working during the pandemic.", options:[{key:"A",text:"eliminate"},{key:"B",text:"embrace"},{key:"C",text:"emerge"},{key:"D",text:"employ"}], answer:"B", explanation:"embrace = 欣然接受。eliminate（消除）、emerge（出现）、employ（雇用）均不表示'积极采纳'。" }],
  essential: [{ id:"cet6_q_essential", type:"single_choice", question:"A balanced diet is ______ for maintaining good health and preventing chronic diseases.", options:[{key:"A",text:"eventual"},{key:"B",text:"excessive"},{key:"C",text:"essential"},{key:"D",text:"external"}], answer:"C", explanation:"be essential for = 对…是必要的。eventual（最终的）、excessive（过度的）、external（外部的）语义不匹配。" }],
  eventually: [{ id:"cet6_q_eventually", type:"single_choice", question:"The negotiations were tough and lasted for months, but both sides ______ reached an agreement.", options:[{key:"A",text:"eventually"},{key:"B",text:"essentially"},{key:"C",text:"extremely"},{key:"D",text:"especially"}], answer:"A", explanation:"eventually = 最终/终于，与'lasted for months'（持续数月）的时间线索相匹配。essentially（本质上）、extremely（极其）、especially（尤其）均不表示时间上的'最终结果'。" }],
  executive: [{ id:"cet6_q_executive", type:"single_choice", question:"As a senior ______ at the software company, he earns a seven-figure salary plus stock options.", options:[{key:"A",text:"executive"},{key:"B",text:"editor"},{key:"C",text:"engineer"},{key:"D",text:"educator"}], answer:"A", explanation:"senior executive = 高级主管。editor、engineer、educator 的薪资层级通常低于senior executive。" }],
  facility: [{ id:"cet6_q_facility", type:"single_choice", question:"The university has invested millions in state-of-the-art laboratory ______ for its science departments.", options:[{key:"A",text:"facilities"},{key:"B",text:"faculties"},{key:"C",text:"factories"},{key:"D",text:"fashions"}], answer:"A", explanation:"laboratory facilities = 实验设施。faculties（学院/院系）虽也在大学语境使用，但'state-of-the-art lab...'最配 facilities。factories（工厂）、fashions（时尚）语义不匹配。" }],
  flexible: [{ id:"cet6_q_flexible", type:"single_choice", question:"The company offers ______ working hours, allowing employees to choose when they start and finish.", options:[{key:"A",text:"flexible"},{key:"B",text:"financial"},{key:"C",text:"fluent"},{key:"D",text:"formal"}], answer:"A", explanation:"flexible working hours = 弹性工作时间，是职场最常见的搭配。financial（财务的）、fluent（流利的）、formal（正式的）均不能修饰'work hours'表示灵活安排。" }],
  fundamental: [{ id:"cet6_q_fundamental", type:"single_choice", question:"Access to clean water is a ______ human right recognized by the United Nations.", options:[{key:"A",text:"flexible"},{key:"B",text:"fundamental"},{key:"C",text:"financial"},{key:"D",text:"fictional"}], answer:"B", explanation:"fundamental human right = 基本人权，是国际法领域的固定术语。flexible（灵活的）、financial（财务的）、fictional（虚构的）均不能修饰'human right'表示'基本的'。" }],
  generate: [{ id:"cet6_q_generate", type:"single_choice", question:"The renewable energy project is expected to ______ enough electricity to power 50,000 households.", options:[{key:"A",text:"generate"},{key:"B",text:"guarantee"},{key:"C",text:"govern"},{key:"D",text:"graduate"}], answer:"A", explanation:"generate electricity = 发电。guarantee（保证）、govern（治理）、graduate（毕业）均不适用于'产生电力'。" }],
  guarantee: [{ id:"cet6_q_guarantee", type:"single_choice", question:"Hard work does not ______ success, but it certainly improves your chances.", options:[{key:"A",text:"guarantee"},{key:"B",text:"generate"},{key:"C",text:"govern"},{key:"D",text:"graduate"}], answer:"A", explanation:"guarantee success = 保证成功。generate（产生）、govern（治理）、graduate（毕业）均不用于'保证某种结果'。" }],
  highlight: [{ id:"cet6_q_highlight", type:"single_choice", question:"The professor's lecture ______ the importance of critical thinking in scientific research.", options:[{key:"A",text:"highlighted"},{key:"B",text:"hesitated"},{key:"C",text:"hospitalized"},{key:"D",text:"humiliated"}], answer:"A", explanation:"highlight the importance = 强调重要性。hesitate（犹豫）、hospitalize（送医住院）、humiliate（羞辱）语义完全不同。" }],
  hypothesis: [{ id:"cet6_q_hypothesis", type:"single_choice", question:"The researchers proposed a new ______ to explain the unexpected decline in bee populations.", options:[{key:"A",text:"hypothesis"},{key:"B",text:"highlight"},{key:"C",text:"hygiene"},{key:"D",text:"harmony"}], answer:"A", explanation:"propose a hypothesis = 提出假说，是科学研究方法论的标准术语。" }],
  identify: [{ id:"cet6_q_identify", type:"single_choice", question:"Scientists have ______ over 50 genes linked to an increased risk of developing Alzheimer's disease.", options:[{key:"A",text:"identified"},{key:"B",text:"ignored"},{key:"C",text:"illustrated"},{key:"D",text:"imitated"}], answer:"A", explanation:"identify genes = 识别/发现基因。ignore（忽视）与句意相反，illustrate（说明）、imitate（模仿）语义不适用。" }],
  implement: [{ id:"cet6_q_implement", type:"single_choice", question:"The government has been slow to ______ the reforms that were promised during the election.", options:[{key:"A",text:"identify"},{key:"B",text:"illustrate"},{key:"C",text:"implement"},{key:"D",text:"imagine"}], answer:"C", explanation:"implement reforms = 实施改革。identify（识别）、illustrate（说明）、imagine（想象）均不涉及政策执行。" }],
  inevitable: [{ id:"cet6_q_inevitable", type:"single_choice", question:"Some degree of job losses in traditional manufacturing is ______ as automation becomes widespread.", options:[{key:"A",text:"invisible"},{key:"B",text:"incredible"},{key:"C",text:"inevitable"},{key:"D",text:"independent"}], answer:"C", explanation:"inevitable = 不可避免的。invisible（不可见的）、incredible（难以置信的）、independent（独立的）语义不匹配。" }],
  justify: [{ id:"cet6_q_justify", type:"single_choice", question:"The government will need to ______ its decision to spend billions on space exploration to the public.", options:[{key:"A",text:"justify"},{key:"B",text:"judge"},{key:"C",text:"jail"},{key:"D",text:"joke"}], answer:"A", explanation:"justify a decision = 为决策辩护/证明其合理性。" }],
  keen: [{ id:"cet6_q_keen", type:"single_choice", question:"The young engineer is extremely ______ to work on the company's most challenging projects.", options:[{key:"A",text:"keen"},{key:"B",text:"kind"},{key:"C",text:"known"},{key:"D",text:"knocked"}], answer:"A", explanation:"be keen to do = 渴望做某事，固定搭配。" }],
  landscape: [{ id:"cet6_q_landscape", type:"single_choice", question:"The regulatory ______ for cryptocurrency has changed dramatically over the past two years.", options:[{key:"A",text:"landscape"},{key:"B",text:"landlord"},{key:"C",text:"language"},{key:"D",text:"landmark"}], answer:"A", explanation:"regulatory landscape = 监管格局/形势，是政策分析领域的比喻用法。" }],
  legislation: [{ id:"cet6_q_legislation", type:"single_choice", question:"Under the new ______, all companies with over 100 employees must publish their gender pay gap data.", options:[{key:"A",text:"legislation"},{key:"B",text:"landscape"},{key:"C",text:"literature"},{key:"D",text:"limitation"}], answer:"A", explanation:"under the new legislation = 根据新法律。landscape（格局）、literature（文学）、limitation（限制）均不适用于法律条文。" }],
  magnificent: [{ id:"cet6_q_magnificent", type:"single_choice", question:"The view from the mountaintop was absolutely ______ — snow-capped peaks stretching as far as the eye could see.", options:[{key:"A",text:"magnificent"},{key:"B",text:"mysterious"},{key:"C",text:"miserable"},{key:"D",text:"minimum"}], answer:"A", explanation:"magnificent = 壮丽的。mysterious（神秘的）、miserable（悲惨的）、minimum（最小的）均不能传达'壮美'。" }],
  motivate: [{ id:"cet6_q_motivate", type:"single_choice", question:"Good managers know that recognition and autonomy ______ employees more effectively than fear.", options:[{key:"A",text:"motivate"},{key:"B",text:"monitor"},{key:"C",text:"modify"},{key:"D",text:"mobilize"}], answer:"A", explanation:"motivate employees = 激励员工，是管理学核心概念。" }],
  negotiate: [{ id:"cet6_q_negotiate", type:"single_choice", question:"Union leaders are ______ with the factory management for better pay and working conditions.", options:[{key:"A",text:"negotiating"},{key:"B",text:"neglecting"},{key:"C",text:"notifying"},{key:"D",text:"nominating"}], answer:"A", explanation:"negotiate with = 与…谈判，是劳资关系场景的标准动词。" }],
  objective: [{ id:"cet6_q_objective", type:"single_choice", question:"The primary ______ of the training program is to improve customer service satisfaction by 20 percent.", options:[{key:"A",text:"objective"},{key:"B",text:"obstacle"},{key:"C",text:"observation"},{key:"D",text:"obligation"}], answer:"A", explanation:"primary objective = 首要目标。obstacle（障碍）、observation（观察）、obligation（义务）均不表示'目标'。" }],
  opponent: [{ id:"cet6_q_opponent", type:"single_choice", question:"The senator was a vocal ______ of the tax reform bill, calling it unfair to middle-class families.", options:[{key:"A",text:"opponent"},{key:"B",text:"opportunity"},{key:"C",text:"operator"},{key:"D",text:"opinion"}], answer:"A", explanation:"a vocal opponent of = 直言不讳的反对者。" }],
  participate: [{ id:"cet6_q_participate", type:"single_choice", question:"All citizens are encouraged to ______ in local elections and have a say in community affairs.", options:[{key:"A",text:"participate"},{key:"B",text:"penetrate"},{key:"C",text:"persuade"},{key:"D",text:"prescribe"}], answer:"A", explanation:"participate in elections = 参与选举。penetrate（穿透）、persuade（说服）、prescribe（开处方）均不能与'elections'搭配。" }],
  phenomenon: [{ id:"cet6_q_phenomenon", type:"single_choice", question:"The rapid spread of smartphones in developing countries is a remarkable social and economic ______.", options:[{key:"A",text:"phenomenon"},{key:"B",text:"philosophy"},{key:"C",text:"photography"},{key:"D",text:"physician"}], answer:"A", explanation:"social phenomenon = 社会现象。" }],
  predominant: [{ id:"cet6_q_predominant", type:"single_choice", question:"Coal remains the ______ source of energy in many developing economies, despite environmental concerns.", options:[{key:"A",text:"predominant"},{key:"B",text:"previous"},{key:"C",text:"precious"},{key:"D",text:"precise"}], answer:"A", explanation:"predominant source = 主要来源。" }],
  qualification: [{ id:"cet6_q_qualification", type:"single_choice", question:"A bachelor's degree is the minimum ______ required for the entry-level position.", options:[{key:"A",text:"qualification"},{key:"B",text:"quality"},{key:"C",text:"quantity"},{key:"D",text:"quotation"}], answer:"A", explanation:"minimum qualification = 最低资格要求。quality（质量）、quantity（数量）、quotation（引语）均不表示'学历资格'。" }],
  recommend: [{ id:"cet6_q_recommend", type:"single_choice", question:"Doctors strongly ______ that adults get at least 150 minutes of moderate exercise each week.", options:[{key:"A",text:"recommend"},{key:"B",text:"recognize"},{key:"C",text:"recover"},{key:"D",text:"reduce"}], answer:"A", explanation:"recommend that = 建议/推荐。" }],
  reluctant: [{ id:"cet6_q_reluctant", type:"single_choice", question:"Despite the high salary offer, the candidate was ______ to relocate to a small town far from family.", options:[{key:"A",text:"reluctant"},{key:"B",text:"reliable"},{key:"C",text:"religious"},{key:"D",text:"remarkable"}], answer:"A", explanation:"be reluctant to = 勉强/不情愿。" }],
  reputation: [{ id:"cet6_q_reputation", type:"single_choice", question:"The university has earned an international ______ for excellence in medical research.", options:[{key:"A",text:"reputation"},{key:"B",text:"regulation"},{key:"C",text:"revolution"},{key:"D",text:"resolution"}], answer:"A", explanation:"earn an international reputation = 赢得国际声誉。" }],
  sacrifice: [{ id:"cet6_q_sacrifice", type:"single_choice", question:"Many parents are willing to ______ their own comfort to give their children a better education.", options:[{key:"A",text:"sacrifice"},{key:"B",text:"satisfy"},{key:"C",text:"schedule"},{key:"D",text:"strengthen"}], answer:"A", explanation:"sacrifice comfort = 牺牲舒适。" }],
  sophisticated: [{ id:"cet6_q_sophisticated", type:"single_choice", question:"Modern smartphones contain highly ______ technology that would have seemed like science fiction 30 years ago.", options:[{key:"A",text:"sophisticated"},{key:"B",text:"sufficient"},{key:"C",text:"suspicious"},{key:"D",text:"superficial"}], answer:"A", explanation:"sophisticated technology = 精密/尖端技术。" }],
  substantial: [{ id:"cet6_q_substantial", type:"single_choice", question:"The company reported a ______ increase in profits, up 45 percent compared to the previous year.", options:[{key:"A",text:"superficial"},{key:"B",text:"substantial"},{key:"C",text:"suspicious"},{key:"D",text:"sufficient"}], answer:"B", explanation:"substantial increase = 大幅增长，与'up 45 percent'的数据相呼应。" }],
  tackle: [{ id:"cet6_q_tackle", type:"single_choice", question:"The new mayor has promised to ______ the city's chronic traffic congestion with a series of bold measures.", options:[{key:"A",text:"tackle"},{key:"B",text:"threaten"},{key:"C",text:"transform"},{key:"D",text:"translate"}], answer:"A", explanation:"tackle traffic congestion = 解决交通拥堵。" }],
  tremendous: [{ id:"cet6_q_tremendous", type:"single_choice", question:"The new treatment has shown ______ potential in early clinical trials, with patients recovering faster than expected.", options:[{key:"A",text:"tremendous"},{key:"B",text:"temporary"},{key:"C",text:"transparent"},{key:"D",text:"typical"}], answer:"A", explanation:"tremendous potential = 巨大的潜力。" }],
  ultimate: [{ id:"cet6_q_ultimate", type:"single_choice", question:"Although the path is difficult, the ______ goal of becoming a doctor has kept her motivated through years of study.", options:[{key:"A",text:"ultimate"},{key:"B",text:"urgent"},{key:"C",text:"urban"},{key:"D",text:"uniform"}], answer:"A", explanation:"ultimate goal = 最终目标。" }],
  valid: [{ id:"cet6_q_valid", type:"single_choice", question:"The discount coupon is only ______ for purchases made before the end of this month.", options:[{key:"A",text:"valid"},{key:"B",text:"vague"},{key:"C",text:"violent"},{key:"D",text:"visible"}], answer:"A", explanation:"valid = 有效的。vague（模糊的）、violent（暴力的）、visible（可见的）均不修饰'到期/有效'概念。" }],
  vulnerable: [{ id:"cet6_q_vulnerable", type:"single_choice", question:"Elderly people living alone are particularly ______ to fraud and financial scams.", options:[{key:"A",text:"vulnerable"},{key:"B",text:"voluntary"},{key:"C",text:"valuable"},{key:"D",text:"violent"}], answer:"A", explanation:"be vulnerable to = 易受…伤害。" }],
  warrant: [{ id:"cet6_q_warrant", type:"single_choice", question:"The judge issued an arrest ______ after new evidence linked the suspect to the crime scene.", options:[{key:"A",text:"warrant"},{key:"B",text:"weapon"},{key:"C",text:"wealth"},{key:"D",text:"welfare"}], answer:"A", explanation:"arrest warrant = 逮捕令，是法律程序的固定术语。" }],
  withstand: [{ id:"cet6_q_withstand", type:"single_choice", question:"The new building material is designed to ______ extreme temperatures, from minus 50 to plus 60 degrees Celsius.", options:[{key:"A",text:"withstand"},{key:"B",text:"withdraw"},{key:"C",text:"witness"},{key:"D",text:"worship"}], answer:"A", explanation:"withstand extreme temperatures = 经受极端温度。" }],
  yield: [{ id:"cet6_q_yield", type:"single_choice", question:"After months of negotiation, the company finally ______ to union demands for higher wages.", options:[{key:"A",text:"yielded"},{key:"B",text:"yawned"},{key:"C",text:"yelled"},{key:"D",text:"yielded"}], answer:"A", explanation:"yield to demands = 屈服于要求，指公司最终向工会加薪要求'让步'。" }],
  zone: [{ id:"cet6_q_zone", type:"single_choice", question:"The coastal ______ has been designated as a marine protected area where fishing is strictly prohibited.", options:[{key:"A",text:"zone"},{key:"B",text:"zoo"},{key:"C",text:"zoom"},{key:"D",text:"zinc"}], answer:"A", explanation:"coastal zone = 沿海地带，与'marine protected area（海洋保护区）'对应。" }]
};

// 3. Build course JSON
const chapters = {};
for (const w of rawWords) {
  const letter = w.Word[0].toUpperCase();
  if (!chapters[letter]) chapters[letter] = [];
  chapters[letter].push(w);
}

const course = {
  course_id: "cet6",
  course_name: "CET6 核心词汇",
  subject_id: "english",
  structure_type: "flat",
  chapters: []
};

const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
for (const letter of letters) {
  const words = chapters[letter] || [];
  if (words.length === 0) continue;

  const knowledgePoints = words.map(w => {
    const wordLower = w.Word.toLowerCase();
    const wordQuizzes = QUIZ_MAP[wordLower] || [];
    // Extract key concepts from meaning
    const concepts = [];
    if (w.Meaning) {
      const parts = w.Meaning.split('；').slice(0, 3);
      for (const p of parts) {
        const m = p.match(/^(n\.|v\.|adj\.|adv\.|vt\.|vi\.|prep\.|n\.\/v\.|n\.\/adj\.)/);
        if (m) {
          const rest = p.substring(m[0].length).split('；')[0].trim().slice(0, 20);
          if (rest) concepts.push(rest);
        } else {
          concepts.push(p.trim().slice(0, 20));
        }
      }
    }

    return {
      id: `cet6_${w.Num}`,
      title: w.Word,
      content_type: "markdown",
      content: `## ${w.Word} ${w.Phonetic}\n\n${w.Meaning}`,
      key_concepts: concepts.filter(Boolean).slice(0, 4),
      quizzes: wordQuizzes
    };
  });

  course.chapters.push({
    id: `cet6_${letter}`,
    title: letter,
    knowledge_points: knowledgePoints
  });
}

// 4. Save
const jsonPath = 'E:/.Claude Code Project/3.知识学习APP_20260528/knowledge_app/assets/content/english_cet6.json';
fs.writeFileSync(jsonPath, JSON.stringify(course, null, 2), 'utf8');

const size = Math.round(fs.statSync(jsonPath).size / 1024);
let quizCount = 0;
for (const ch of course.chapters) {
  for (const kp of ch.knowledge_points) {
    quizCount += kp.quizzes.length;
  }
}

console.log(`Generated ${jsonPath}`);
console.log(`  Words: ${rawWords.length}`);
console.log(`  Chapters: ${course.chapters.length} (A-Z)`);
console.log(`  Quizzes: ${quizCount}`);
console.log(`  File size: ${size} KB`);
