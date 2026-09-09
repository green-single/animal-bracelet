// 模拟测试：领养后旅程成就逻辑
// 场景1：未领养 → globe/thousand/border 都不解锁（即使历史距离25772km）
// 场景2：领养时间=最新轨迹时间之后 → 领养后距离≈0，不解锁
// 场景3：领养时间在轨迹中间 → 只算领养后的距离

// 从animal.html提取旅程成就代码段做逻辑验证（只验证算法，不跑浏览器）
function haversine(lat1, lon1, lat2, lon2) {
  var R = 6371;
  var dLat = (lat2-lat1)*Math.PI/180;
  var dLon = (lon2-lon1)*Math.PI/180;
  var a = Math.sin(dLat/2)*Math.sin(dLat/2) +
    Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*
    Math.sin(dLon/2)*Math.sin(dLon/2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// 模拟数据：5个点，每点相距约1000km（故意造大距离）
var points = [[0,0],[9,0],[18,0],[27,0],[36,0]]; // 每9度约1000km
var timestamps = ['2024-01-01 00:00:00','2024-02-01 00:00:00','2024-03-01 00:00:00','2024-04-01 00:00:00','2024-05-01 00:00:00'];

function calcJourney(adoptedDateStr, animalId, localStorageStore) {
  var adoptedInfo = adoptedDateStr ? {date: adoptedDateStr} : null;
  var adoptedDate = adoptedInfo && adoptedInfo.date ? new Date(adoptedInfo.date) : null;
  var startIdx = 0;
  if (adoptedDate) {
    var foundIdx = -1;
    for (var tix = 0; tix < timestamps.length; tix++) {
      if (new Date(timestamps[tix].replace(' ','T')) >= adoptedDate) { foundIdx = tix; break; }
    }
    if (foundIdx === -1) {
      startIdx = points.length;
    } else {
      startIdx = Math.max(0, foundIdx - 1);
    }
  } else {
    startIdx = points.length;
  }
  var totalDist = 0;
  if (points.length > startIdx + 1) {
    for (var di = startIdx + 1; di < points.length; di++) {
      totalDist += haversine(points[di][0], points[di][1], points[di-1][0], points[di-1][1]);
    }
  }
  return {startIdx: startIdx, totalDist: totalDist,
    globe: adoptedDate && totalDist >= 10000,
    thousand: adoptedDate && totalDist >= 5000,
    border: adoptedDate && points.length > startIdx + 1};
}

// 场景1：未领养
var r1 = calcJourney(null);
console.log('场景1 未领养:', JSON.stringify(r1));
console.log('  断言: 都不解锁 →', r1.globe===false && r1.thousand===false && r1.border===false ? 'PASS' : 'FAIL');

// 场景2：领养时间在2024-03-01（中间）
var r2 = calcJourney('2024-03-01T00:00:00');
console.log('场景2 领养在中途:', JSON.stringify(r2));
console.log('  断言: startIdx=2(03-01前一个点)，距离=2000km左右，thousand不达标 →',
  r2.startIdx===2 && r2.thousand===false && r2.globe===false && r2.border===false ? 'PASS' : 'FAIL');

// 场景3：领养时间在2024-05-01之后（新数据还没来）
var r3 = calcJourney('2024-06-01T00:00:00');
console.log('场景3 领养在数据之后:', JSON.stringify(r3));
console.log('  断言: startIdx=5(无点可算)，距离=0 →', r3.startIdx===5 && r3.totalDist===0 ? 'PASS' : 'FAIL');

// 场景4：领养在2024-01-01（最开头）→ 算全部距离4000km，border应解锁(跨36度>20)
var r4 = calcJourney('2024-01-01T00:00:00');
console.log('场景4 领养在最前:', JSON.stringify(r4));
console.log('  断言: startIdx=0，全距离~4000km，border解锁 →', r4.startIdx===0 && r4.border===true && r4.thousand===false ? 'PASS' : 'FAIL');
