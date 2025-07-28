<script>
	import { tick } from 'svelte';

	// Form state
	let formData = $state({
		product_name: '',
		brand_name: '',
		category: [],
		price: '',
		discounted_price: '',
		description: '',
		product_url: '',
		ad_type: 'social_media',
		ad_tone: 'professional'
	});

	// UI state
	let isGenerating = $state(false);
	let generatedAd = $state('');
	let isStreaming = $state(false);
	let copySuccess = $state(false);
	let categoryInput = $state('');
	let responseExpanded = $state(true);
	let wordCount = $state(0);

	// imagen
	let generateImage = $state(false);
	let imageLoading = $state(false);
	let generatedImageUrl = $state(null);
	let imageError = $state(null);


	// Form validation
	let errors = $state({});

	const validateForm = () => {
		const newErrors = {};
		
		if (!formData.product_name.trim()) newErrors.product_name = 'Product name is required';
		if (!formData.brand_name.trim()) newErrors.brand_name = 'Brand name is required';
		if (formData.category.length === 0) newErrors.category = 'At least one category is required';
		if (!formData.price || formData.price <= 0) newErrors.price = 'Valid price is required';
		if (!formData.description.trim()) newErrors.description = 'Description is required';
		
		errors = newErrors;
		return Object.keys(newErrors).length === 0;
	};

	const addCategory = () => {
		if (categoryInput.trim() && !formData.category.includes(categoryInput.trim())) {
			formData.category = [...formData.category, categoryInput.trim()];
			categoryInput = '';
		}
	};

	const removeCategory = (index) => {
		formData.category = formData.category.filter((_, i) => i !== index);
	};

	const handleCategoryKeydown = (event) => {
		if (event.key === 'Enter') {
			event.preventDefault();
			addCategory();
		}
	};

	// imagen api
	const generateImageAPI = async () => {
		try {
			imageLoading = true;
			imageError = null;
			
			const response = await fetch('http://127.0.0.1:8000/api/v1/generate-image', {
				method: 'POST',
				headers: {
					'accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					product_name: formData.product_name,
					brand_name: formData.brand_name,
					description: formData.description
				})
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const imageData = await response.json();
		
			if (imageData.image_path) {
				const imageFileName = imageData.image_path.split('/').pop();
				generatedImageUrl = `http://127.0.0.1:8000/api/v1/images/${imageFileName}`;
			} else {
				throw new Error('No image path received from API');
			}
		
		} catch (error) {
			console.error('Image generation error:', error);
			imageError = error.message;
			generatedImageUrl = null;
		} finally {
			imageLoading = false;
		}
	};

	// retry
	const retryImageGeneration = () => {
		imageError = null;
		generateImageAPI();
	};

	const generateAd = async () => {
		if (!validateForm()) return;

		isGenerating = true;
		isStreaming = true;
		generatedAd = '';
		responseExpanded = true;

		try {
			// Run ad generation and image generation in parallel
			const tasks = [
				fetch('http://127.0.0.1:8000/api/v1/generate-stream', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(formData)
				}),
				generateImage ? generateImageAPI() : Promise.resolve()
			];

			const [adResponse] = await Promise.all(tasks);

			if (!adResponse.body) throw new Error('No response body');

			const reader = adResponse.body.getReader();
			const decoder = new TextDecoder();
			let done = false;

			while (!done) {
				const { value, done: doneReading } = await reader.read();
				done = doneReading;
				if (value) {
					const chunk = decoder.decode(value);
					const lines = chunk.split('\n').filter(line => line.trim() !== '');
					for (const line of lines) {
						try {
							const parsed = JSON.parse(line);
							if (parsed.status === 'streaming' && parsed.content) {
								generatedAd += parsed.content;
								await tick();
								const responseArea = document.getElementById('response-area');
								if (responseArea) {
									responseArea.scrollTop = responseArea.scrollHeight;
								}
							}
						} catch (err) {
							console.error('Failed to parse streaming response:', err);
						}
					}
				}
			}
			wordCount = generatedAd.trim().split(/\s+/).filter(word => word.length > 0).length;
		} catch (err) {
			console.error('Streaming error:', err);
			generatedAd = '[ERROR] ' + (err instanceof Error ? err.message : 'Unknown error');
		} finally {
			isGenerating = false;
			isStreaming = false;
		}
	};

	const copyToClipboard = async () => {
		try {
			await navigator.clipboard.writeText(generatedAd);
			copySuccess = true;
			setTimeout(() => copySuccess = false, 2000);
		} catch (err) {
			console.error('Failed to copy text: ', err);
		}
	};

	const clearResponse = () => {
		generatedAd = '';
		responseExpanded = false;
		wordCount = 0;
		generatedImageUrl = null;
		imageError = null;
		generateImage = false;
	};

</script>

<div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
   <div class="container mx-auto px-2 py-2 max-w-10xl">
		<!-- Header Section -->
		<header class="text-center mb-12">
			<div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl mb-6 shadow-lg">
				<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
				</svg>
			</div>
			<h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-4">
				AI Ad Generator
			</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
				Transform your product details into compelling, conversion-focused advertisements using the power of artificial intelligence
			</p>
		</header>

		<!-- Main Content -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
		   <!-- Form Section -->
		   <div class="bg-white/80 backdrop-blur-md rounded-3xl p-10 shadow-2xl border border-white/30 flex flex-col justify-between lg:col-span-1 lg:min-h-[600px]">
				<h2 class="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
					<svg class="w-6 h-6 mr-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
					</svg>
					Product Details
				</h2>

				<form onsubmit={event => { event.preventDefault(); generateAd(); }} class="space-y-6">
					<!-- Product Name -->
					<div>
						<label for="product_name" class="block text-sm font-medium text-gray-700 mb-2">Product Name *</label>
						<input
							id="product_name"
							type="text"
							bind:value={formData.product_name}
							placeholder="e.g., Karlsburg Men's Solid Formal Shirt"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							class:border-red-300={errors.product_name}
						/>
						{#if errors.product_name}
							<p class="text-red-500 text-sm mt-1">{errors.product_name}</p>
						{/if}
					</div>

					<!-- Brand Name -->
					<div>
						<label for="brand_name" class="block text-sm font-medium text-gray-700 mb-2">Brand Name *</label>
						<input
							id="brand_name"
							type="text"
							bind:value={formData.brand_name}
							placeholder="e.g., Alice Bag"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							class:border-red-300={errors.brand_name}
						/>
						{#if errors.brand_name}
							<p class="text-red-500 text-sm mt-1">{errors.brand_name}</p>
						{/if}
					</div>

					<!-- Category -->
					<div>
						<label for="category" class="block text-sm font-medium text-gray-700 mb-2">Categories *</label>
						<div class="space-y-3">
							<div class="flex">
								<input
									id="category"
									type="text"
									bind:value={categoryInput}
									onkeydown={handleCategoryKeydown}
									placeholder="Add a category and press Enter"
									class="flex-1 px-4 py-3 rounded-l-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
								/>
								<button
									type="button"
									onclick={addCategory}
									class="px-4 py-3 bg-blue-500 text-white rounded-r-xl hover:bg-blue-600 transition-colors duration-200"
									aria-label="Add Category"
								>
									Add
								</button>
							</div>
							{#if formData.category.length > 0}
								<div class="flex flex-wrap gap-2">
									{#each formData.category as cat, index}
										<span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
											{cat}
											<button
												type="button"
												onclick={() => removeCategory(index)}
												class="ml-2 text-blue-600 hover:text-blue-800"
												aria-label="Remove Category"
											>
												×
											</button>
										</span>
									{/each}
								</div>
							{/if}
						</div>
						{#if errors.category}
							<p class="text-red-500 text-sm mt-1">{errors.category}</p>
						{/if}
					</div>

					<!-- Price Fields -->
					<div class="grid md:grid-cols-2 gap-4">
						<div>
							<label for="price" class="block text-sm font-medium text-gray-700 mb-2">Price ($) *</label>
							<input
								id="price"
								type="number"
								step="0.01"
								min="0"
								bind:value={formData.price}
								placeholder="45.00"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
								class:border-red-300={errors.price}
							/>
							{#if errors.price}
								<p class="text-red-500 text-sm mt-1">{errors.price}</p>
							{/if}
						</div>
						<div>
							<label for="discounted_price" class="block text-sm font-medium text-gray-700 mb-2">Sale Price ($)</label>
							<input
								id="discounted_price"
								type="number"
								step="0.01"
								min="0"
								bind:value={formData.discounted_price}
								placeholder="30.00"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							/>
						</div>
					</div>

					<!-- Description -->
					<div>
						<label for="description" class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
						<textarea
							id="description"
							bind:value={formData.description}
							placeholder="Describe your product's key features and benefits..."
							rows="4"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
							class:border-red-300={errors.description}
						></textarea>
						{#if errors.description}
							<p class="text-red-500 text-sm mt-1">{errors.description}</p>
						{/if}
					</div>

					<!-- Image Generation -->
					 <div>
						<label class="block text-sm font-medium text-gray-700 mb-3">
							Generate Image?
							<button
								type="button"
								class="ml-2 text-gray-400 hover:text-gray-600"
								title="Image generation takes 10-30 seconds"
								aria-label="Image generation takes 10-30 seconds"
							>
								<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
							</button>
						</label>
						<div class="flex space-x-6">
							<label class="flex items-center">
								<input
									type="radio"
									bind:group={generateImage}
									value={true}
									class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2"
								/>
								<span class="ml-2 text-sm font-medium text-gray-700">Yes</span>
							</label>
							<label class="flex items-center">
								<input
									type="radio"
									bind:group={generateImage}
									value={false}
									class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2"
								/>
								<span class="ml-2 text-sm font-medium text-gray-700">No</span>
							</label>
						</div>
						
						{#if generateImage && imageLoading}
							<div class="mt-3 flex items-center text-blue-600">
								<svg class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
								<span class="text-sm">Generating image... Please wait (10-30 seconds)</span>
							</div>
						{/if}
						
						{#if imageError}
							<div class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
								<div class="flex items-center">
									<svg class="w-4 h-4 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
									</svg>
									<span class="text-sm text-red-700">Failed to generate image</span>
								</div>
								<div class="mt-2 flex space-x-2">
									<button
										type="button"
										onclick={retryImageGeneration}
										class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200 transition-colors duration-200"
										aria-label="Retry Image Generation"
									>
										Retry
									</button>
									<button
										type="button"
										onclick={() => { generateImage = false; imageError = null; }}
										class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200 transition-colors duration-200"
										aria-label="Continue without Image Generation"
									>
										Continue without
									</button>
								</div>
							</div>
						{/if}
					</div>

					<!-- URLs -->
					<div class="space-y-4">
						<div>
							<label for="product_url" class="block text-sm font-medium text-gray-700 mb-2">Product URL</label>
							<input
								id="product_url"
								type="url"
								bind:value={formData.product_url}
								placeholder="https://example.com/product-page"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							/>
						</div>
					</div>
 
					<!-- Configuration -->
					<div class="grid md:grid-cols-2 gap-4">
						<div>
							<label for="ad_type" class="block text-sm font-medium text-gray-700 mb-2">Ad Type</label>
							<select
								id="ad_type"
								bind:value={formData.ad_type}
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							>
								<option value="social_media">Social Media</option>
								<option value="email">Email</option>
								<option value="product_description">Product Description</option>
							</select>
						</div>
						<div>
							<label for="ad_tone" class="block text-sm font-medium text-gray-700 mb-2">Ad Tone</label>
							<select
								id="ad_tone"
								bind:value={formData.ad_tone}
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							>
								<option value="professional">Professional</option>
								<option value="friendly">Friendly</option>
								<option value="urgent">Urgent</option>
								<option value="luxurious">Luxurious</option>
								<option value="playful">Playful</option>
								<option value="minimalist">Minimalist</option>
								<option value="bold">Bold</option>
								<option value="conversational">Conversational</option>
							</select>
						</div>
					</div>

					<!-- Generate Button -->
					<button
						type="submit"
						disabled={isGenerating}
						class="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-blue-600 hover:to-indigo-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
						aria-label="Generate Ad"
					>
						{#if isGenerating}
							<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							Generating...
						{:else}
							<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
							</svg>
							Generate Ad
						{/if}
					</button>
				</form>
			</div>

			<!-- AI Response Section -->
			<div class="bg-white/90 backdrop-blur-md rounded-3xl shadow-2xl border border-white/30 flex flex-col lg:col-span-1 lg:min-h-[50%] h-auto">
				<div class="p-6 border-b border-gray-100">
					<div class="flex items-center justify-between">
						<h2 class="text-2xl font-semibold text-gray-800 flex items-center">
							<svg class="w-6 h-6 mr-3 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 01-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
							</svg>
							Generated Ad
						</h2>
						<button
							onclick={() => responseExpanded = !responseExpanded}
							class="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
							aria-label="Toggle Response"
						>
							<svg class="w-5 h-5 transform transition-transform duration-200" class:rotate-180={!responseExpanded} fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
							</svg>
						</button>
					</div>
					{#if generatedAd}
						<div class="flex items-center justify-between mt-2">
							<p class="text-sm text-gray-500">{wordCount} words</p>
							<div class="flex space-x-2">
								<button
									onclick={copyToClipboard}
									class="inline-flex items-center px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors duration-200"
									class:bg-green-200={copySuccess}
									aria-label="Copy Ad"
								>
									{#if copySuccess}
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Copied!
									{:else}
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
										</svg>
										Copy
									{/if}
								</button>
								<button
									onclick={clearResponse}
									class="inline-flex items-center px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
									aria-label="Clear Response"
								>
									<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
									</svg>
									Clear
								</button>
							</div>
						</div>
					{/if}
				</div>
				{#if responseExpanded}
					<div class="flex-1 p-2 overflow-y-auto">
						{#if !generatedAd && !isGenerating}
							<div class="flex flex-col items-center justify-center h-64 text-gray-400">
								<svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
								</svg>
								<p class="text-lg font-medium">Your AI-generated ad will appear here</p>
								<p class="text-sm">Fill out the form and click "Generate Ad" to get started</p>
							</div>
						{:else}
							<div
							   id="response-area"
							   class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 min-h-[50vh] max-h-[50vh] overflow-y-auto"
							>
								{#if isGenerating && !generatedAd}
									<div class="flex items-center text-gray-500">
										<svg class="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
											<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
											<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
										</svg>
										AI is crafting your perfect ad...
									</div>
								{:else if generatedAd}
									<div class="prose prose-gray max-w-none">
										<textarea
											class="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed bg-transparent border border-gray-300 rounded-md p-2 w-full resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 h-[40vh]"
											bind:value={generatedAd}
										></textarea>
										{#if isStreaming}
											<span class="inline-block w-2 h-5 bg-blue-500 animate-pulse ml-1"></span>
										{/if}
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/if}
				{#if generatedImageUrl}
					<div class="mt-1">
						<h3 class="text-lg font-medium text-gray-800 mb-3 flex items-center">
							<svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
							</svg>
							Generated Image:
						</h3>
						<div class="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
							<img
								src={generatedImageUrl || "/placeholder.svg"}
								alt={`Generated image for ${formData.product_name} by ${formData.brand_name}`}
								class="w-full max-w-sm mx-auto rounded-lg shadow-md"
								style="max-height: 300px; object-fit: contain;"
								onload={() => console.log('Image loaded successfully')}
								onerror={() => {
									console.error('Failed to load generated image');
									imageError = 'Failed to load generated image';
									generatedImageUrl = null;
								}}
							/>
							<div class="mt-3 flex justify-center">
								<a
									href={generatedImageUrl}
									download={`${formData.product_name}_${formData.brand_name}_ad_image.png`}
									class="inline-flex items-center px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors duration-200"
								>
									<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
									</svg>
									Download Image
								</a>
							</div>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>

<style>
	:global(body) {
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}
</style>

