// 简化版 Babel 帮助函数：将可迭代/类数组对象转为真正的数组
// 这里只实现项目当前需要的核心功能，避免引入完整的 @babel/runtime 依赖

function toConsumableArray(arr) {
  if (Array.isArray(arr)) {
    // 普通数组，直接浅拷贝
    return arr.slice();
  }

  // 支持常见可迭代对象（如 Set、Map 的 keys/values 等）
  if (typeof Symbol !== 'undefined' && arr != null && (arr[Symbol.iterator] || arr['@@iterator'])) {
    return Array.from(arr);
  }

  // 支持简单的类数组对象（例如 arguments、NodeList 等）
  if (arr && typeof arr.length === 'number') {
    var result = new Array(arr.length);
    for (var i = 0; i < arr.length; i++) {
      result[i] = arr[i];
    }
    return result;
  }

  // 其他情况返回空数组，避免运行时报错
  return [];
}

module.exports = toConsumableArray;


