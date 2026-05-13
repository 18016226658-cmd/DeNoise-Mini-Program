// utils/algorithms.js
// 说明：大整数分解算法已经全部迁移到 Python 后端。
// 这里仅保留「输入校验」等轻量级前端逻辑，避免和后端算法混淆。

/**
 * 验证输入是否为有效的大整数（前端版本，只做格式和长度检查）
 * @param {String|Number} input - 用户输入
 * @returns {{valid: boolean, number: BigInt|null, error: string|null}}
 */
function validateInput(input) {
  if (input === null || input === undefined) {
    return { valid: false, number: null, error: '请输入数字' };
  }

  const str = String(input);
  const trimmed = str.trim();

  if (!trimmed) {
    return { valid: false, number: null, error: '请输入数字' };
  }

  // 只允许 0-9
  const cleaned = trimmed.replace(/[^0-9]/g, '');
  if (!cleaned) {
    return { valid: false, number: null, error: '请输入数字（0-9）' };
  }

  // 只能是纯数字
  if (!/^[0-9]+$/.test(cleaned)) {
    return { valid: false, number: null, error: '只能输入数字0-9，不能包含字母或特殊字符' };
  }

  // 前导零（允许单个 0）
  if (cleaned.length > 1 && cleaned[0] === '0') {
    return { valid: false, number: null, error: '数字不能有前导零' };
  }

  // 位数限制（与后端保持一致，最多 200 位）
  if (cleaned.length > 200) {
    return { valid: false, number: null, error: '数字位数不能超过200位' };
  }

  try {
    const num = BigInt(cleaned);
    return { valid: true, number: num, error: null };
  } catch (e) {
    return { valid: false, number: null, error: '数字格式错误，无法解析为大整数' };
  }
}

// 以下函数仅为兼容旧代码的占位实现，真正的算法逻辑已迁移到 Python 后端。
// 小程序当前不会在前端进行大整数分解，只做基础展示，因此这里给出简单占位实现，避免报错。

function millerRabin(n, k = 3) {
  // 仅用于快速类型提示，返回 false 表示“暂时当作合数/未知”，实际结果以后端为准
  try {
    const num = BigInt(n);
    if (num === 2n || num === 3n) return true;
    if (num < 2n || num % 2n === 0n) return false;
  } catch (e) {
    return false;
  }
  return false;
}

function getNumberType(n, factors) {
  // 占位：前端不再依赖此结果，实际类型以后端返回为准
  return { type: 'unknown', typeName: '未知', description: '数字类型由后端判断' };
}

function getFactorizationLevel(originalNumber, factors) {
  // 占位：前端不再在本地判断分解程度，实际结果以后端返回为准
  return { level: 'unknown', levelName: '未知', description: '分解程度由后端判断' };
}

module.exports = {
  validateInput,
  millerRabin,
  getNumberType,
  getFactorizationLevel
};


