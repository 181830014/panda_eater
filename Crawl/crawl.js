var cheerio = require('cheerio')
var rp = require('request-promise')
var fs = require('fs')

var tot = 0

async function requestCont(filename, myurl)
{
    let options = {
        url : myurl,
        timeout : 10000
    }
    try{
        let body = await rp(options)
        tot += 1
        console.log('链接成功：' + myurl + '\n' + tot.toString() + '\n')
        let $ = cheerio.load(body)
        let desc = $('.bz_first_comment').find('pre').text().trim()
        console.log(filename + myurl.slice(-6) + '.txt')
        fs.writeFile(filename + myurl.slice(-6) + '.txt', desc, (err) => {});
    }catch (e) {
        console.log('链接失败，错误信息：' + e)
    }
}

var geneURL = function(IDs)
{
    var head = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id='
    let URLs = []
    for(i = 0; i < IDs.length; i++)
        URLs.push(head + IDs[i])
    return URLs
}

async function __main()
{
    let l_title = ['bz_P1', 'bz_P2', 'bz_P3', 'bz_P4', 'bz_P5']
    let l_level = ['bz_normal', 'bz_critical', 'bz_enhancement', 'bz_major', 'bz_trivial']
    let l_url = [
        'https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=P1',
        'https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=P2',
        'https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&field0-0-0=priority&limit=300&no_redirect=1&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&query_format=advanced&type0-0-0=anyexact&value0-0-0=P3',
        'https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=P4',
        'https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=P5',
    ]

    for(let i = 0; i < l_title.length; i++)
        for(let j = 0; j < l_level.length; j++)
            fs.mkdir('./results/' + l_title[i] + '_' + l_level[j] , { recursive: true }, (err) => {
                if (err) throw err;
            });

    for(let i = 0; i < l_title.length; i++) {
        console.log('尝试拉取列表 ...')
        let done = false
        let $ = undefined
        while(done === false) {
            let options = {
                url : l_url[i],
                timeout : 20000
            }
            try{
                let home = await rp(options)
                $ = cheerio.load(home)
                done = true
                console.log(l_title[i] + '列表拉取成功')
            }catch (e) {
                console.log('链接失败，错误信息：' + e)
            }
        }
        
        for(let j = 0; j < l_level.length; j++) {
            let IDs = []
            pattern = '.' + l_title[i] + '.' + l_level[j]
            $(pattern).find('a').each(function(i, e) {
                if(i % 2 == 0) IDs.push($(e).text().trim())
                // else console.log($(e).text().trim())
            });
            console.log(pattern + ':' + IDs.length.toString() + '\n')
            let URLs = geneURL(IDs)
            for (let k = 0; k < URLs.length; k++) {
                requestCont('./results/' + l_title[i] + '_' + l_level[j] + '/', URLs[k])
            }
        }
    }
}

__main()