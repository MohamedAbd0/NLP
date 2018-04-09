using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Task_Japan
{
    public partial class Form1 : Form
    {
       
        StringBuilder txt = new StringBuilder();
        IDictionary<string, string> Hiragana = new Dictionary<string, string>() {
                                                              
            {"ka", "か"},{"ki", "き"},{"ku", "く"},{"ke", "け"},{"ko", "こ"},{"sa", "さ"},{"shi", "し"},{"su", "す"},
            {"se", "せ"},{"so", "そ"},{"ta", "た"},{"chi", "ち"},{"tsu", "つ"},{"te", "て"},{"to", "と"},{"na", "な"},
            {"ni", "に"},{"nu", "ぬ"},{"ne", "ね"},{"no", "の"},{"ha", "は"},{"hi", "ひ"},{"fu", "ふ"},{"he", "へ"},
            {"ho", "ほ"},{"ma", "ま"},{"mi", "み"},{"mu", "む"},{"me", "め"},{"mo", "も"},{"ya", "や"},{"yu", "ゆ"},
            {"yo", "よ"},{"ra", "ら"},{"ri", "り"},{"ru", "る"},{"re", "れ"},{"ro", "ろ"},{"wa", "わ"},{"wo", "を"},{"wn", "ん"},
            {"gi","ぎ"},{"gu","ぐ"},{"ge","げ"},{"go","ご"},{"za","ざ"},{"ji","じ"},{"zu","ず"},{"ze","ぜ"},{"zo","ぞ"},
            {"da","だ"},{"jｉ","ぢ"},{"dｅ","で"},{"do","ど"},{"ba","ば"},{"bｉ","び"},{"bu","ぶ"},{"bｅ","べ"},
            {"bo","ぼ"},{"pa","ぱ"},{"pｉ","ぴ"},{"pu","ぷ"},{"pｅ","ぺ"},{"po","ぽ"},
            {"kya","きゃ"},{"kyu","きゅ"},{"kyo","きょ"},{"sha","しゃ"},{"shu","しゅ"},{"sho","しょ"},{"cha","ちゃ"},{"chu","ちゅ"},
            {"cho","ちょ"},{"nya","にゃ"},{"nyu","にゅ"},{"nyo","にょ"},{"hya","ひゃ"},{"hyu","ひゅ"},{"hyo","ひょ"},{"mya","みゃ"},
            {"myu","みゅ"},{"myo","みょ"},{"rya","りゃ"},{"ryu","りゅ"},{"ryo","りょ"},{"gya","ぎゃ"},{"gyu","ぎ"},{"gyo","ぎょ"},
            {"ja","じゃ"},{"ju","じゅ"},{"jo","じょ"},{"bya","びゃ"},{"byu","びゅ"},{"byo","びょ"},{"pya","ぴゃ"},{"pyu","ぴゅ"},{"pyo","ぴょ"},
            { "a", "あ"},{"i", "い"},{"u", "う"},{"e", "え"},{"o", "お"} ,{" "," "}  
        };

        IDictionary<string, string> Katakana = new Dictionary<string, string>()
        {
        {"ka","カ"},{"kｉ","キ"},{"ku","ク"},{"kｅ","ケ"},{"ko","コ"},{"sa","サ"},{"shｉ","シ"},{"su","ス"},
        {"sｅ","セ"},{"so","ソ"},{"ta","タ"},{"chｉ","チ"},{"tsu","ツ"},{"tｅ","テ"},{"to","ト"},{"na","ナ"},
        {"nｉ","ニ"},{"nu","ヌ"},{"nｅ","ネ"},{"no","ノ"},{"ha","ハ"},{"hi","ヒ"},{"Ｆu","フ"},{"hｅ","ヘ"},
        {"ho","ホ"},{"ma","マ"},{"mｉ","ミ"},{"mu","ム"},{"mｅ","メ"},{"mo","モ"},{"ya","ヤ"},{"yu","ユ"},
        {"yo","ヨ"},{"ra","ラ"},{"ri","リ"},{"ru","ル"},{"rｅ","レ"},{"ro","ロ"},{"wa","ワ"},{"wo","ヲ"},
        {"ga","ガ"},{"gi","ギ"},{"gu","グ"},{"gｅ","ゲ"},{"go","ゴ"},{"za","ザ"},{"ji","ジ"},
        {"zｅ","ゼ"},{"zo","ゾ"},{"da","ダ"},{"jｉ","ヂ"},{"zu","ヅ"},{"dｅ","デ"},{"do","ド"},{"ba","バ"},
        {"bｉ","ビ"},{"bu","ブ"},{"bｅ","ベ"},{"bo","ボ"},{"pa","パ"},{"pｉ","ピ"},{"pu","プ"},{"pｅ","ペ"},
        {"po","ポ"},{"kya","ギャ"} ,{"kyu","ギュ"} ,{"kyo","ギョ"} ,{"sha","シャ"} ,{"shu","シュ"} ,{"she","シェ"}  ,{"sho","ショ"} ,
        {"cha","チャ"} ,{"chu","チュ"} ,{"che","チェ"}  ,{"cho","チョ"} ,{"nya","ニャ"} ,{"nyu","ニュ"} ,{"nyo","ニョ"} ,{"hya","ヒャ"} ,
        {"hyu","ヒュ"} ,{"hyo","ヒョ"} ,{"mya","ミャ"} ,{"myu","ミュ"} ,{"myo","ミョ"} ,{"rya","リャ"} ,
        {"ryu","リュ"} ,{"ryo","リョ"} ,{"gya","ギャ"} ,{"gyu","ギュ"} ,{"gyo","ギョ"} ,{"ja","ジャ"},{"ju","ジュ"},{"je","ジェ"} , 
        {"jo","ジョ"},{"bya","ビャ"} ,{"byu","ビュ"} ,{"byo","ビョ"} ,{"pya","ピャ"} ,{"pyu","ピュ"} ,{"pyo","ピョ"},
        {"a","ア"},{"i","イ"},{"u","ウ"},{"e","エ"},{"o","オ"} ,{" "," "}
            };

        string flag = "";
       
        public Form1()
        {
            InitializeComponent();
            
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            flag = "";
            flag = "Hiragana";
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            flag = "";
            flag = "Katakana";
        }

        //to translat from en to japan
        public void translate(IDictionary<string,string> dc)
        {
            foreach (KeyValuePair<string, string> item in dc)
            {
                txt.Replace(item.Key, item.Value);
            }
        }
        //to translat from  japan to en
        public void Invers_Translate(IDictionary<string, string> dc)
        {
            foreach (KeyValuePair<string, string> item in dc)
            {
                txt.Replace(item.Value, item.Key);
            }
        }


        private void button1_Click(object sender, EventArgs e)
        {
            txt.Clear();
            txt.Append(richTextBox1.Text.ToLower());

            if (lbltype.Text == "En -> Japan")
            {
                if (flag == "Hiragana")
                    translate(Hiragana);
                else if (flag == "Katakana")
                    translate(Katakana);
                else
                    MessageBox.Show("PLZ select The Type Of Language ");

            }
            else
            {
                if (flag == "Hiragana")
                    Invers_Translate(Hiragana);
                else if (flag == "Katakana")
                    Invers_Translate(Katakana);
                else
                    MessageBox.Show("PLZ select The Type Of Language ");
            }

            label1.Text = txt.ToString();

        }

        private void lbltype_Click(object sender, EventArgs e)
        {
            richTextBox1.Text =label1.Text= "";
            if (lbltype.Text == "En -> Japan")
            {
                lbltype.Text = "Japan -> En";
                Color pgcolor = lbltype.BackColor;
                lbltype.BackColor = lbltype.ForeColor;
                lbltype.ForeColor = pgcolor;

            }
            else
            {
                lbltype.Text = "En -> Japan";
                Color pgcolor = lbltype.BackColor;
                lbltype.BackColor = lbltype.ForeColor;
                lbltype.ForeColor = pgcolor;
            }
        }
    }
}
