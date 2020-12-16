var request = require('request')
var cheerio = require('cheerio')
var rp = require('request-promise')
var fs = require('fs')

var tot = 0

async function requestCont(filename, url)
{
    let body = await rp(url)
    console.log('链接成功：' + url + '\n' + tot.toString() + '\n')
    tot += 1
    let $ = cheerio.load(body)
    let desc = $('.bz_first_comment').find('pre').text().trim()
    fs.appendFileSync(filename, '7498217498122 URL = ' + url + '\n\n' + desc + '\n\n')
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
    let l_first = ['bz_normal', 'bz_critical', 'bz_enhancement', 'bz_major', 'bz_trivial']
    let l_second = ['bz_P1', 'bz_P2', 'bz_P3', 'bz_P4', 'bz_P5']

    // let home = await rp('https://bugs.eclipse.org/bugs/buglist.cgi?chfield=%5BBug%20creation%5D&chfieldfrom=7d')
    let home = await rp('https://bugs.eclipse.org/bugs/buglist.cgi?chfield=%5BBug%20creation%5D&chfieldfrom=1m')
    let $ = cheerio.load(home)
    console.log('列表拉取成功')

    for(let i = 0; i < l_first.length; i++) {
        for(let j = 0; j < l_second.length; j++) {
            // let fd = fs.openSync('./results/' + l_second[j] + '_' + l_first[i] + '.txt', 'r+');
            // fs.ftruncateSync(fd)
            let IDs = []
            pattern = '.' + l_first[i] + '.' + l_second[j]
            $(pattern).find('a').each(function(i, e) {
                if(i % 2 == 0) IDs.push($(e).text().trim())
            });
            console.log(pattern + ':' + IDs.length.toString() + '\n')
            let URLs = geneURL(IDs)
            for (let k = 0; k < URLs.length; k++) 
                requestCont('./results/' + l_second[j] + '_' + l_first[i] + '.txt', URLs[k])
        }
    }
}

__main()