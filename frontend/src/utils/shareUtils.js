// Simple QR code generator for WeChat sharing
export function generateQRCode(text, size = 200) {
  // This is a placeholder for QR code generation
  // In production, you would use a proper QR code library
  return new Promise((resolve) => {
    const canvas = window.document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    canvas.width = size
    canvas.height = size
    
    // Draw placeholder QR code
    ctx.fillStyle = '#000'
    ctx.fillRect(0, 0, size, size)
    ctx.fillStyle = '#fff'
    ctx.fillRect(10, 10, size - 20, size - 20)
    
    // Draw some pattern to simulate QR code
    const blockSize = 10
    for (let i = 0; i < size / blockSize - 2; i++) {
      for (let j = 0; j < size / blockSize - 2; j++) {
        if (Math.random() > 0.5) {
          ctx.fillStyle = '#000'
          ctx.fillRect(10 + i * blockSize, 10 + j * blockSize, blockSize - 2, blockSize - 2)
        }
      }
    }
    
    resolve(canvas.toDataURL())
  })
}

// Generate share URL for different platforms
export function generateShareUrl(platform, data) {
  const { title, description, url } = data
  
  switch (platform) {
    case 'weibo':
      return `https://service.weibo.com/share/share.php?title=${encodeURIComponent(title + ' ' + description)}&url=${encodeURIComponent(url)}`
    
    case 'qq':
      return `https://connect.qq.com/widget/shareqq/index.html?title=${encodeURIComponent(title)}&summary=${encodeURIComponent(description)}&url=${encodeURIComponent(url)}`
    
    case 'douyin':
      // Douyin doesn't have direct web sharing, so we return the URL for manual sharing
      return `https://www.douyin.com/`
    
    default:
      return url
  }
}

// Copy text to clipboard
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    // Fallback for older browsers
    const textArea = window.document.createElement('textarea')
    textArea.value = text
    window.document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    window.document.body.removeChild(textArea)
    return true
  }
}
