# -*- coding: utf-8 -*-
"""重构灯箱openLightbox：去掉pre-load，直接设src（与照片墙一致），加超时兜底"""
with open('app/static/animal.html', 'rb') as f:
    c = f.read()

def crlf(s):
    return s.replace('\n', '\r\n')

old = crlf("""  _lbIndex = idx;
  var img = document.getElementById('lbImg');
  var spinner = document.getElementById('lbSpinner');
  // 显示加载状态
  img.classList.add('loading');
  spinner.classList.add('show');
  // 预加载图片
  var pre = new Image();
  pre.onload = function() {
    img.src = _lbPhotos[idx];
    img.classList.remove('loading');
    spinner.classList.remove('show');
    img.onload = function() { img.classList.remove('loading'); spinner.classList.remove('show'); };
  };
  pre.onerror = function() {
    img.src = _lbPhotos[idx];
    img.classList.remove('loading');
    spinner.classList.remove('show');
  };
  pre.src = _lbPhotos[idx];
  document.getElementById('lbCounter').textContent = (idx + 1) + ' / ' + _lbPhotos.length;
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
  // 图片加载完成后自动适应
  img.onload = function() { img.classList.remove('loading'); spinner.classList.remove('show'); };
}""").encode('utf-8')

new = crlf("""  _lbIndex = idx;
  var img = document.getElementById('lbImg');
  var spinner = document.getElementById('lbSpinner');
  var url = _lbPhotos[idx] || '';
  // 每次打开清理上次的缩放状态
  img.style.transform = '';
  img.style.maxWidth = '';
  img.style.maxHeight = '';
  // 显示加载状态
  img.classList.add('loading');
  spinner.classList.add('show');
  // 与照片墙一致：直接设置 src（同URL照片墙能显示，灯箱必然能显示）
  img.onload = function() {
    img.classList.remove('loading');
    spinner.classList.remove('show');
  };
  img.onerror = function() {
    img.classList.remove('loading');
    spinner.classList.remove('show');
    img.alt = '照片加载失败，请检查网络后重试';
  };
  // 超时兜底：2.5秒后强制显示，避免一直转圈
  clearTimeout(img._lbTimer);
  img._lbTimer = setTimeout(function() {
    img.classList.remove('loading');
    spinner.classList.remove('show');
  }, 2500);
  img.src = url;
  document.getElementById('lbCounter').textContent = (idx + 1) + ' / ' + _lbPhotos.length;
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
}""").encode('utf-8')

if old not in c:
    print('❌ 未找到目标代码块，检查实际内容')
    i = c.find(b'var pre = new Image()')
    print(c[max(0,i-300):i+600])
else:
    c = c.replace(old, new, 1)
    with open('app/static/animal.html', 'wb') as f:
        f.write(c)
    print('✓ 灯箱已重构')
